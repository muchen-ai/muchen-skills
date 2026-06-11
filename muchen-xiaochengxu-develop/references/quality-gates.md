# Quality Gates

Run the gates that match the task. For full project handoff, run all of them.

## Backend

```bash
cd muchen-server
mvn -pl :muchen-server -am -DskipTests package
```

Smoke checks after startup:

- `GET http://localhost:48080/actuator/health`
- Login with tenant `沐辰平台`, user `admin`, password `admin123`
- Changed `/admin-api` endpoints
- Changed `/app-api` endpoints

## Admin Frontend

```bash
cd muchen-admin-front
pnpm install --frozen-lockfile
pnpm ts:check
pnpm build:local
```

Browser checks:

- `http://localhost:80`
- Login succeeds
- Changed menu opens without server error
- Console error count is zero for changed pages

## Mini Program

```bash
cd muchen-app
pnpm install --frozen-lockfile
pnpm build:h5
pnpm build:mp-weixin
```

Browser checks:

- `http://localhost:3000`
- Home/decorate template loads
- Changed H5 pages render
- No “未找到模板” error

## Docker

```bash
docker compose -f docker-compose.local.yml up -d --build
docker compose -f docker-compose.local.yml ps
```

If MySQL initialization must be retested from empty state:

```bash
docker compose -f docker-compose.local.yml down -v
docker compose -f docker-compose.local.yml up -d --build
```

## Residue Scan

Run from repo root:

```bash
find . -maxdepth 4 \( -name node_modules -o -name dist -o -name target -o -name output -o -name '.DS_Store' -o -name '*.zip' -o -name '.pnpm-store' \) -print
rg -n --hidden --glob '!**/.git/**' --glob '!**/node_modules/**' --glob '!**/dist/**' --glob '!**/target/**' '新星慧享|shopro|JeecgBoot|yudao-ui-admin|api-dashboard\.yudao|static-vue3\.yudao|test\.yudao'
```

Allowed residue must be explicitly explained in the final response.
