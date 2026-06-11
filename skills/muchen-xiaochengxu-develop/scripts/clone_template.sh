#!/usr/bin/env bash
set -euo pipefail

REMOTE="git@github.com:muchen-ai/muchen-plateform.git"
TEMPLATE_REF="template-v1.0.0"
KEEP_GIT=0

usage() {
  cat <<'USAGE'
Usage:
  clone_template.sh <target-dir> [--template-ref REF] [--remote GIT_URL] [--keep-git]

Defaults:
  --template-ref template-v1.0.0
  --remote git@github.com:muchen-ai/muchen-plateform.git

The target directory must not exist or must be empty. By default, template Git history is removed
after cloning so the new business project can use its own repository.
USAGE
}

if [[ $# -eq 1 && ( "${1:-}" == "-h" || "${1:-}" == "--help" ) ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

TARGET_DIR="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --template-ref)
      TEMPLATE_REF="${2:-}"
      shift 2
      ;;
    --remote)
      REMOTE="${2:-}"
      shift 2
      ;;
    --keep-git)
      KEEP_GIT=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$TARGET_DIR" || -z "$REMOTE" || -z "$TEMPLATE_REF" ]]; then
  echo "target-dir, remote, and template-ref must be non-empty." >&2
  exit 2
fi

if [[ -e "$TARGET_DIR" ]]; then
  if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Target exists and is not a directory: $TARGET_DIR" >&2
    exit 1
  fi
  if [[ -n "$(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
    echo "Target directory is not empty: $TARGET_DIR" >&2
    exit 1
  fi
fi

mkdir -p "$(dirname "$TARGET_DIR")"

echo "Cloning muchen template..."
echo "  remote: $REMOTE"
echo "  ref:    $TEMPLATE_REF"
echo "  target: $TARGET_DIR"

git -c advice.detachedHead=false clone --branch "$TEMPLATE_REF" --depth 1 "$REMOTE" "$TARGET_DIR"

if [[ "$KEEP_GIT" -eq 0 ]]; then
  rm -rf "$TARGET_DIR/.git"
  echo "Removed template Git history from $TARGET_DIR"
else
  echo "Kept template Git history in $TARGET_DIR"
fi

echo "Done. Next: replace project name, logo, domain, database name, tenant, and README values."
