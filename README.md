# muchen-skills

English | [中文](./README.zh.md)

Agent skills for developing projects on the `muchen` mini program template platform.

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
git@four.github.com:muchen-ai/muchen-plateform.git
```

Skill source:

```text
./skills/muchen-xiaochengxu-develop
```

## Validation

```bash
sh scripts/validate-skills.sh
```

Audit a local template project:

```bash
npm run audit:template
```
