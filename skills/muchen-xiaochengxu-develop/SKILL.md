---
name: muchen-xiaochengxu-develop
description: Develop mini program projects on the muchen template platform. Use when creating a new business project from the muchen template, adding full-stack business modules to an existing muchen-server/muchen-admin-front/muchen-app workspace, wiring backend/admin/mini-program APIs, SQL, Docker, documentation, tests, and cleanup for a reusable 小程序 development base.
---

# muchen Mini Program Development

Use this skill to create or extend projects based on the `muchen` mini program template platform.

## Quick Start

1. Decide whether the user is starting a new project or modifying an existing muchen project.
2. For a new project, run `scripts/clone_template.sh <target-dir>` to copy `template-v1.0.0`.
3. For an existing project, run `scripts/audit_muchen_project.sh <project-dir>` before editing.
4. Read only the references needed for the task:
   - Template facts and invariants: `references/template-contract.md`
   - Required development phases: `references/development-workflow.md`
   - Where to add backend/admin/mini-program code: `references/extension-patterns.md`
   - Required checks before handoff: `references/quality-gates.md`

## Non-Negotiable Rules

- Keep the template source outside this skill. Always clone from the template Git tag.
- Do not put business logic into `system`, `infra`, `member`, or `app` foundation modules.
- Do not enable payment, approval, mall, CRM, ERP, AI, IoT, or other heavy modules by default.
- Do not commit `node_modules`, `dist`, `target`, `.DS_Store`, zip backups, screenshots, or local cache folders.
- Keep Java packages as `cn.iocoder.yudao` unless the user explicitly requests a full package migration.
- Update root and three-end README files when creating a new business project or adding a significant module.

## Default Workflow

Follow these phases and report progress after each substantial phase:

1. Understand the user's business requirement and split backend, admin, mini-program, SQL, Docker, and documentation impact.
2. Initialize from the template if no project exists; otherwise audit the current project first.
3. Rename business-visible values: project name, logo, domain, database name, default tenant, app config, README.
4. Add backend code in a separate business module and expose `/admin-api` and `/app-api` endpoints as needed.
5. Add admin API clients, views, routes, menus, permissions, and validation in the business domain.
6. Add mini-program API clients, pages, stores, and components in the business domain.
7. Add SQL initialization and Docker changes needed for a clean empty-database startup.
8. Run quality gates, browser checks, residue scans, and cleanup before committing.

## Script Usage

Clone a new project from the template:

```bash
<skill-dir>/scripts/clone_template.sh /path/to/new-project
```

Audit a project:

```bash
<skill-dir>/scripts/audit_muchen_project.sh /path/to/project
```

Treat audit warnings as implementation tasks unless the user explicitly accepts them.
