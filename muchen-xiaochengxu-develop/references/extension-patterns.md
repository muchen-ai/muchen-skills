# Extension Patterns

Use these patterns when adding new business capability.

## Backend

- Create a separate module named `yudao-module-<biz>`.
- Keep controller paths under `/admin-api/<biz>` and `/app-api/<biz>`.
- Keep business tables prefixed by `<biz>_`.
- Add menu permissions and dictionary data in SQL.
- Wire the new module into the server POM only after it builds independently.

Do not add business services directly into foundation modules unless the change is truly generic platform capability.

## Admin Frontend

- API clients: `muchen-admin-front/src/api/<biz>`
- Views: `muchen-admin-front/src/views/<biz>`
- Routes and menu entries must match backend permissions.
- Use existing table, form, dialog, upload, dictionary, and request utilities.
- Keep operational UI dense and task-focused.

## Mini Program

- API clients: `muchen-app/sheep/api/<biz>`
- Pages: `muchen-app/pages/<biz>`
- Stores: use existing Pinia/store conventions where needed.
- Reuse request, auth, upload, WebView, error page, layout, tabbar, and decorate rendering foundation.
- Keep H5 and WeChat mini-program builds valid for V1.

## SQL

- Add `<biz>_schema.sql` for business tables and seed data.
- Keep `muchen-server/sql/init/muchen_platform_mysql_init.sql` importable from an empty database.
- Include menu, permission, dictionary, and default data needed for first login.
- Do not rename existing member `point_trade_*` columns unless the user accepts a migration.

## Naming

- Use lowercase English project identifiers for directories, containers, database names, and images.
- Use Chinese display names for UI titles when the user provides them.
- Replace logo, title, tenant, share text, and domain values during project initialization.
