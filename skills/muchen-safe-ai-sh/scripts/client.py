#!/usr/bin/env python3
"""Prepare and use a host-specific SSH identity, or bootstrap from a human terminal."""

import argparse
import base64
import binascii
import io
import ipaddress
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

SCRIPTS = Path(__file__).resolve().parent
STATE = Path.home() / ".muchen-safe-ai-sh"
ACCOUNT = "muchen-diag"
CERT_TYPE = b"ssh-ed25519-cert-v01@openssh.com"


def private_dir(path):
    if path.is_symlink():
        raise ValueError(f"Refusing a symlink for private state: {path}")
    path.mkdir(mode=0o700, exist_ok=True)
    info = path.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError(f"Private state must be owned by you and mode 0700: {path}")


def host_dir(alias):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,62}", alias):
        raise ValueError("Use a short alias containing letters, digits, underscores or hyphens.")
    private_dir(STATE)
    return STATE / alias


def verify_address(host, port):
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]{0,252}", host):
            raise ValueError("Provide a bare SSH hostname or IP address.") from None
    if "%" in host or not 1 <= port <= 65535:
        raise ValueError("Use an unscoped address and an SSH port between 1 and 65535.")


def registration(alias):
    directory = host_dir(alias)
    if not directory.is_dir():
        raise ValueError(f"Run prepare for alias {alias!r} first.")
    private_dir(directory)
    config = json.loads((directory / "host.json").read_text(encoding="utf-8"))
    verify_address(config["host"], config["port"])
    key = directory / "client"
    if not stat.S_ISREG(key.lstat().st_mode) or key.stat().st_mode & 0o077:
        raise ValueError(f"Invalid private key permissions: {key}")
    return directory, config


def prepare(args):
    verify_address(args.host, args.port)
    directory = host_dir(args.alias)
    config = {"host": args.host, "port": args.port}
    try:
        directory.mkdir(mode=0o700)
    except FileExistsError:
        directory, existing = registration(args.alias)
        if existing != config:
            raise ValueError("This alias belongs to another endpoint. Choose a new alias.")
    else:
        try:
            subprocess.run(
                ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C",
                 f"muchen-safe-ai-sh:{args.alias}", "-f", str(directory / "client")],
                check=True,
            )
            (directory / "host.json").write_text(json.dumps(config) + "\n", encoding="utf-8")
        except BaseException:
            shutil.rmtree(directory)
            raise
    sys.stdout.write((directory / "client.pub").read_text(encoding="ascii"))


def bundle_files(directory):
    return [(SCRIPTS / name, name) for name in ("install-server", "ops-access", "diagnose")] + [
        (directory / "client.pub", "client.pub")
    ]


def bundle(args):
    directory, _ = registration(args.alias)
    output = args.output.expanduser()
    output.mkdir(mode=0o700)
    for source, name in bundle_files(directory):
        shutil.copy2(source, output / name)
    print(output.resolve())


def ssh_options(config):
    # Read the standard known_hosts files, but bypass per-user ProxyJump, forwards and SSH aliases.
    return [
        "ssh", "-F", "/dev/null", "-p", str(config["port"]),
        "-o", "StrictHostKeyChecking=yes", "-o", "UpdateHostKeys=no",
        "-o", "ForwardAgent=no", "-o", "ClearAllForwardings=yes",
        "-o", "ConnectTimeout=8", "-o", "ServerAliveInterval=5", "-o", "ServerAliveCountMax=2",
    ]


def bootstrap(args):
    if not sys.stdin.isatty():
        raise ValueError("Run bootstrap in your own interactive terminal to enter SSH or sudo credentials.")
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_.-]{0,63}", args.admin):
        raise ValueError("Provide the SSH administrator username without a host or options.")
    directory, config = registration(args.alias)
    target = f"{args.admin}@{config['host']}"
    archive = io.BytesIO()
    files = bundle_files(directory)
    with tarfile.open(fileobj=archive, mode="w:gz") as output:
        for source, name in files:
            output.add(source, arcname=name, recursive=False)
    payload = base64.b64encode(archive.getvalue()).decode("ascii")

    command = ["/bin/bash"]
    if args.admin != "root":
        command[:0] = ["sudo", "-k", "--"]
    install = shlex.join(command) + ' "$work/install-server"'
    for name in ("default_seconds", "max_seconds"):
        value = getattr(args, name)
        if value is not None:
            install += " --" + name.replace("_", "-") + " " + str(value)
    cleanup_files = " ".join(f'"$work/{name}"' for _, name in files)
    remote = f"""set -euo pipefail
umask 077
work=$(mktemp -d /tmp/muchen-safe-ai-sh.XXXXXXXX)
trap 'rm -f -- {cleanup_files}; rmdir -- "$work"' EXIT
trap 'exit 1' HUP INT TERM
printf '%s' '{payload}' | base64 -d | tar --no-same-owner -xzf - -C "$work"
{install}
"""
    # A single foreground SSH connection leaves no administrator socket to reuse.
    request = shlex.join(["/bin/bash", "-c", remote])
    if len(request) > 60000:
        raise ValueError("Installer too large for one SSH command. Use bundle for manual transport.")
    options = ssh_options(config) + [
        "-tt", "-o", "ControlMaster=no", "-o", "ControlPath=none", "-o", "IdentityAgent=none",
        "-o", "PubkeyAuthentication=no", "-o", "PreferredAuthentications=keyboard-interactive,password",
    ]
    subprocess.run(options + [target, request], check=True)

def diagnose(args):
    directory, config = registration(args.alias)
    with args.certificate.open("rb") as stream:
        data = stream.read(16385)
    line = data.strip()
    fields = line.split(None, 2)
    if len(data) > 16384 or b"\n" in line or b"\r" in line or len(fields) < 2 or fields[0] != CERT_TYPE:
        raise ValueError("Provide a file containing exactly one Ed25519 SSH public certificate.")
    try:
        base64.b64decode(fields[1], validate=True)
    except binascii.Error:
        raise ValueError("Malformed SSH public certificate.") from None

    with tempfile.TemporaryDirectory(prefix="msha-cert-") as work:
        # OpenSSH associates a sibling certificate with its IdentityFile even when
        # cert-only algorithm filtering removes the ordinary public-key identity.
        identity = Path(work) / "client"
        identity.symlink_to(directory / "client")
        cert = Path(work) / "client-cert.pub"
        cert.write_bytes(line + b"\n")
        cert.chmod(0o600)
        options = ssh_options(config) + [
            "-T", "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes", "-o", "IdentityAgent=none",
            "-o", "ControlMaster=no", "-o", "ControlPath=none",
            "-o", "PreferredAuthentications=publickey",
            "-o", "PubkeyAcceptedAlgorithms=" + CERT_TYPE.decode("ascii"),
            "-i", str(identity),
        ]
        subprocess.run(options + [f"{ACCOUNT}@{config['host']}"], check=True, timeout=30)


def positive(value):
    if not value.isascii() or not value.isdecimal() or int(value) < 1:
        raise argparse.ArgumentTypeError("Expected a positive whole number.")
    return int(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="command", required=True)
    init = modes.add_parser("prepare", help="Register a target and print its local Ed25519 public key.")
    init.add_argument("alias")
    init.add_argument("host")
    init.add_argument("--port", type=positive, default=22)
    init.set_defaults(run=prepare)
    pack = modes.add_parser("bundle", help="Write a public-only installer bundle for manual transport.")
    pack.add_argument("alias")
    pack.add_argument("output", type=Path)
    pack.set_defaults(run=bundle)
    install = modes.add_parser("bootstrap", help="Install using a human-operated terminal.")
    install.add_argument("alias")
    install.add_argument("admin")
    install.add_argument("--default-seconds", type=positive)
    install.add_argument("--max-seconds", type=positive)
    install.set_defaults(run=bootstrap)
    check = modes.add_parser("diagnose", help="Run the registered host's fixed diagnostic.")
    check.add_argument("alias")
    check.add_argument("certificate", type=Path)
    check.set_defaults(run=diagnose)
    args = parser.parse_args()
    try:
        args.run(args)
    except subprocess.CalledProcessError as error:
        print(f"muchen-safe-ai-sh: {args.command} failed (exit {error.returncode}). See the output above.", file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print(f"muchen-safe-ai-sh: {args.command} timed out.", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError) as error:
        print(f"muchen-safe-ai-sh: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
