# muchen-skills

[English](./README.md) | 中文

面向沐辰小程序开发和临时 SSH 诊断的 Agent Skills 仓库。

## 安装

注册为插件市场：

```bash
/plugin marketplace add muchen-ai/muchen-skills
```

安装插件：

```bash
/plugin install muchen-skills@muchen-skills
```

如果使用 skills CLI：

```bash
npx skills add muchen-ai/muchen-skills
```

## 可用 Skills

### muchen-xiaochengxu-develop

用于基于 `muchen` 模板创建和开发小程序全栈项目。

适用场景：

- 从 `muchen-plateform` 的 `template-v1.0.0` tag 创建新业务项目。
- 替换项目名、Logo、域名、数据库名、默认租户和 README。
- 开发后端、后台、小程序三端业务模块。
- 补齐 SQL、Docker、浏览器自测和清理扫描。

模板来源：

```text
git@github.com:muchen-ai/muchen-plateform.git
```

Skill 目录：

```text
./skills/muchen-xiaochengxu-develop
```

### muchen-safe-ai-sh

为指定的 Linux 服务器初始化只读诊断账号。管理员从自己的终端完成首次安装，之后运行 `sudo ops-access` 或 `sudo ops-access 45m`，把输出的一行 SSH 证书交给 Codex 即可发起授权诊断。

[Skill](./skills/muchen-safe-ai-sh/SKILL.md) · [安装与运维手册](./skills/muchen-safe-ai-sh/references/operator-guide.md)

## 验证

```bash
sh scripts/validate-skills.sh
```

审计本地模板项目：

```bash
npm run audit:template
```
