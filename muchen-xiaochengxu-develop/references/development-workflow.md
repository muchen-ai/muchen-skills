# Development Workflow

Follow this workflow for every muchen mini program development task.

## Phase 0: Requirement Split

Before editing, identify:

- Backend APIs and tables
- Admin pages, menus, permissions, and API clients
- Mini-program pages, API clients, stores, and components
- SQL initialization impact
- Docker and environment variable impact
- README and user-facing documentation impact

If a requirement is ambiguous and the repo cannot answer it, ask the user before implementing.

## Phase 1: Project Setup

For new projects:

- Run `scripts/clone_template.sh <target-dir>`.
- Rename business-visible values only after clone succeeds.
- Remove template Git history unless the user asks to keep it.

For existing projects:

- Run `scripts/audit_muchen_project.sh <project-dir>`.
- Read the existing README and Docker compose before changing code.
- Respect uncommitted user changes.

## Phase 2: Implementation

- Add business code in isolated business domains.
- Keep foundation modules generic.
- Prefer existing framework patterns and local helpers.
- Keep frontend pages usable rather than landing-page-like.
- Keep mini-program pages focused on actual workflows.
- Update SQL and menus together with code.

## Phase 3: Verification

Run the narrowest checks that prove the changed behavior, then run the full quality gates when the task is substantial or before handoff.

Always include:

- API smoke checks for changed backend endpoints
- Admin browser check for changed admin menus/pages
- H5 browser check for changed mini-program pages
- Residue scan for junk and old template/business names

## Phase 4: Handoff

Before final response or commit:

- Clean local build artifacts from the repo.
- Update README files when commands, ports, modules, or setup changed.
- Summarize exact checks run and any residual warnings.
