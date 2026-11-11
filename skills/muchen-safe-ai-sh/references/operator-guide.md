# 沐辰临时 SSH 诊断手册

服务器安装一次后，你只需要运行 `sudo ops-access`，把标准输出中的一行 SSH 证书发给 Codex。用 `sudo ops-access 45m` 或 `sudo ops-access 2h` 可指定本次时长。Codex 使用本机保管的连接私钥访问已登记的目标，SSH 仅运行预设的诊断命令。

## 准备目标

- 客户端需要 Python 3 和 OpenSSH，并和 Codex 共用同一个本机用户。目标机需运行 Linux、Python 3，以及可重新加载的 systemd `ssh.service` 或 `sshd.service`。安装器要求 SSH 使用标准 `/etc/ssh/sshd_config`，且有效配置为 `UsePAM yes`。
- 在 Codex 中说明你要初始化的服务器别名、主机名或 IP、SSH 端口、管理员用户名。SSH 和 sudo 密码在你自己的终端输入。
- 先从云控制台或其他可信管理渠道取得目标的 SSH 主机指纹。若服务器提供 Ed25519 主机公钥，管理员可在该服务器上运行 `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` 查看指纹。
- 将核实后的主机公钥登记到本机 OpenSSH 的 `known_hosts`。必须匹配登记时使用的主机名和端口。通过网络扫描得到的公钥只能作为候选，需先与可信指纹核对。主机密钥变更时，先独立确认变更再更新本机记录。

## 首次安装

下面的命令在本 Skill 目录下执行。实际使用时，Codex 可提供包含脚本绝对路径的命令。示例别名为 `app-test`。

```bash
python3 scripts/client.py prepare app-test server.example.com --port 22
python3 scripts/client.py bootstrap app-test admin
```

`prepare` 在当前本机用户的 `~/.muchen-safe-ai-sh/app-test/` 保存登记信息和专用 Ed25519 连接密钥。只需要将其中的连接公钥交给服务器。以后使用同一别名时，应继续保留这把本机私钥。换电脑或丢失私钥时，由管理员按本文回退并重新部署诊断入口，再登记新的连接公钥。

`bootstrap` 在你的终端通过 SSH 连接目标机，上传安装包、执行安装并清理临时文件。SSH 使用密码或键盘交互认证。仅开放公钥登录的目标请使用下文的手动安装包流程。普通管理员账号还需能执行 sudo，终端可能分别提示 SSH 和 sudo 密码。安装程序创建非 root 的 `muchen-diag` 账号、服务器专用 CA 和撤销列表，安装 `/usr/local/bin/ops-access` 与固定诊断程序。安装器在 `/etc/ssh/sshd_config` 首行加入 `Include /etc/muchen-safe-ai-sh/sshd.conf`，专用规则仅匹配 `muchen-diag`。若该主机已有冲突配置，先由管理员检查冲突。保留现有管理入口，直到确认临时诊断已生效。

默认签发 30 分钟，上限为 8 小时。首次安装时可按需要设置这两个值，单位为秒，默认值须小于或等于上限。以下示例设置为默认 45 分钟、最长 2 小时。

```bash
python3 scripts/client.py bootstrap app-test admin --default-seconds 2700 --max-seconds 7200
```

重试前先核对终端最后的安装结果。对于同一台主机与同一把连接公钥，使用同样的参数重新运行。若安装程序报告不同公钥或未托管文件的冲突，按提示由管理员处理，避免覆盖既有配置。

### 手动安装

目标只能由你的跳板机访问，或管理员仅能用公钥登录时，在 Codex 本机生成安装包。你使用现有管理通道把整目录放到目标机的管理员私有临时目录，确认文件来自本次生成的安装包后再执行。

```bash
python3 scripts/client.py bundle app-test ./app-test-bootstrap
```

在目标机的管理员终端中执行安装脚本。目录路径替换成你实际上传的位置，按需追加有效期选项。包内包含安装脚本、签发脚本、诊断程序和客户端公钥。

```bash
sudo /bin/bash /path/to/app-test-bootstrap/install-server
```

安装和核验完成后，可删除上传的临时安装包。若 Codex 所在的机器无法直达目标机，你在目标机运行 `/usr/local/libexec/muchen-safe-ai-sh/diagnose`，把输出发给 Codex。证书提供认证能力，目标机的网络可达性仍由你的管理通道决定。

## 日常签发和诊断

```bash
sudo ops-access
sudo ops-access 45m
sudo ops-access 2h
```

每次选择一条命令执行即可。root 登录时可以省略 `sudo`。自定义时长采用正整数加 `m` 或 `h`，受管理员配置的上限限制。成功签发时，标准输出只是一行 OpenSSH 公钥证书。将这一行原样发给 Codex。如果当前对话已经明确指定了一台服务器，只发证书即可。涉及多台服务器时，同时注明本次要检查的目标别名。证书是公开格式，仍应按本次运维流程传给连接方。连接私钥由 Codex 本机保管，CA 私钥由目标服务器的管理员保管。

Codex 将证书保存到临时文件后执行以下命令。诊断输出 UTC 时间、主机名、内核版本、系统负载、内存和根文件系统用量。诊断账号无 sudo，SSH 服务端限制交互终端、文件传输和转发。该入口用于判断故障现象，变更配置或恢复服务由你在自己的管理会话中执行。

```bash
python3 scripts/client.py diagnose app-test /path/to/ops-access-cert.pub
```

证书和 SSH 目标主机的密钥是两种不同的凭据。服务器验证本次证书和连接私钥，本机验证登记过的主机指纹。证书的生效与到期使用服务器时钟，检查时间不符时先校准时间。

## 审计和撤销

每张证书有唯一序列号。管理员可查阅 `/etc/muchen-safe-ai-sh/grants.json` 中的签发与撤销记录，并与 SSH 认证日志比对。若持有证书文件，也可使用 `ssh-keygen -Lf /path/to/ops-access-cert.pub` 查看序列号和有效期。

```bash
sudo ops-access revoke 1
```

把 `1` 替换为要撤销的序列号。服务器依据 OpenSSH 撤销列表拒绝该证书的新认证，正常到期也会阻止新连接。证书到期或撤销不会主动断开已建立的会话。需要立即终止时，由管理员结束对应的 `muchen-diag` 会话。

## 上线检查与回退

1. 保留自己的管理会话，签发一张短时证书验证正常诊断。
2. 核对证书只用于目标主机的 `muchen-diag` 账号，交互 Shell、SFTP 和端口转发均不可用。验证到期或撤销后，建立新连接会被拒绝。
3. 确认你的管理入口仍能正常登录，再单独撤销原来的 root SSH 公钥授权。更改 root 密码后，已经获准的 SSH 公钥仍可用于公钥认证。
4. 需要回退时，保持自己的管理会话开启，清空 `/etc/muchen-safe-ai-sh/authorized_keys` 以收回专用 CA 信任。结束该账号的诊断会话，再删除专用的 `muchen-diag` 账号。备份并编辑 `/etc/ssh/sshd_config`，只移除安装器加入的 `Include /etc/muchen-safe-ai-sh/sshd.conf`。通过 `sshd -t` 后重新加载对应的 `ssh.service` 或 `sshd.service`，再验证管理员仍能新建连接。最后可归档签发记录并移除专用状态目录、诊断脚本和 `/usr/local/bin/ops-access`。

[OpenSSH 证书签发与 KRL](https://man.openbsd.org/ssh-keygen.1) · [OpenSSH 主机密钥校验](https://man.openbsd.org/ssh_config.5#StrictHostKeyChecking) · [OpenSSH 授权密钥选项](https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT)
