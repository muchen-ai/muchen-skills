# Template Contract

Use these facts as the default contract for `muchen` template projects.

## Source

- Template repository: `git@github.com:muchen-ai/muchen-plateform.git`
- Default template ref: `template-v1.0.0`
- The skill repository must not vendor or copy the template source.

## Project Shape

- `muchen-server`: Spring Boot backend, default port `48080`
- `muchen-admin-front`: Vue admin frontend, default port `80`
- `muchen-app`: uni-app H5 / WeChat mini program, H5 default port `3000`
- Backend API prefixes stay `/admin-api` and `/app-api`.
- Java package names stay `cn.iocoder.yudao`.

## Local Defaults

- Database: MySQL 8
- Database name: `muchen_platform`
- Redis: `redis:7-alpine`
- Docker entry: `docker compose -f docker-compose.local.yml up -d --build`
- Default tenant: `沐辰平台`
- Default admin account: `admin / admin123`

## Foundation Modules

Keep these as platform foundation:

- `system`
- `infra`
- `member`
- `app`

Do not implement business behavior inside these modules. Add new business code in a separate business domain.

## Excluded By Default

Do not enable or reintroduce these modules unless the user explicitly asks and accepts the added scope:

- payment
- BPM / approval
- mall / trade / promotion
- CRM
- ERP
- AI
- IoT
- MES / WMS
- IM / MP

## Initialization SQL

- Total MySQL init script: `muchen-server/sql/init/muchen_platform_mysql_init.sql`
- Docker split scripts:
  - `muchen-server/sql/mysql/quartz.sql`
  - `muchen-server/sql/mysql/muchen_platform.sql`
  - `muchen-server/sql/mysql/member_schema.sql`
- New business schemas should be added as dedicated SQL files and included in the total init path or Docker init flow.
