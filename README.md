# muchen-skills

English | [中文](./README.zh.md)

Agent skills for muchen mini program development and temporary SSH diagnostics.

## Installation

Register this repository as a plugin marketplace:

```bash
/plugin marketplace add muchen-ai/muchen-skills
```

Install the marketplace plugin:

```bash
/plugin install muchen-skills@muchen-skills
```

If using the skills CLI:

```bash
npx skills add muchen-ai/muchen-skills
```

## Available Skills

### muchen-xiaochengxu-develop

Creates and develops mini program projects from the `muchen` template platform.

Use it when you need to:

- Clone `muchen-plateform` from `template-v1.0.0`.
- Rename a copied business project.
- Add backend, admin frontend, and mini-program business modules.
- Wire SQL, Docker, README, browser checks, and cleanup scans.

Template source:

```text
git@github.com:muchen-ai/muchen-plateform.git
```

Skill source:

```text
./skills/muchen-xiaochengxu-develop
```

### muchen-safe-ai-sh

Sets up a read-only SSH diagnosis account on a designated Linux server. The administrator initializes it from a local terminal, then runs `sudo ops-access` or `sudo ops-access 45m` and shares the one-line SSH certificate for the authorized check.

[Skill](./skills/muchen-safe-ai-sh/SKILL.md) · [Operator guide](./skills/muchen-safe-ai-sh/references/operator-guide.md)

## Validation

```bash
sh scripts/validate-skills.sh
```

Audit a local template project:

```bash
npm run audit:template
```
