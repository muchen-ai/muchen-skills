#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  audit_muchen_project.sh <project-dir>

Runs read-only checks for a muchen template project. The script exits non-zero when required
structure is missing or forbidden residue is found.
USAGE
}

if [[ $# -eq 1 && ( "${1:-}" == "-h" || "${1:-}" == "--help" ) ]]; then
  usage
  exit 0
fi

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

ROOT="$1"
ERRORS=0
WARNINGS=0

fail() {
  echo "[FAIL] $*"
  ERRORS=$((ERRORS + 1))
}

warn() {
  echo "[WARN] $*"
  WARNINGS=$((WARNINGS + 1))
}

pass() {
  echo "[ OK ] $*"
}

require_path() {
  local path="$1"
  if [[ -e "$ROOT/$path" ]]; then
    pass "$path exists"
  else
    fail "$path missing"
  fi
}

if [[ ! -d "$ROOT" ]]; then
  echo "Project directory does not exist: $ROOT" >&2
  exit 2
fi

echo "Auditing muchen project: $ROOT"

require_path "muchen-server"
require_path "muchen-admin-front"
require_path "muchen-app"
require_path "docker-compose.local.yml"
require_path "README.md"
require_path "muchen-server/README.md"
require_path "muchen-admin-front/README.md"
require_path "muchen-app/README.md"
require_path "muchen-server/sql/init/muchen_platform_mysql_init.sql"
require_path "muchen-server/sql/mysql/quartz.sql"
require_path "muchen-server/sql/mysql/muchen_platform.sql"
require_path "muchen-server/sql/mysql/member_schema.sql"

if command -v find >/dev/null 2>&1; then
  junk=$(find "$ROOT" -maxdepth 4 \( -name node_modules -o -name dist -o -name target -o -name output -o -name '.DS_Store' -o -name '*.zip' -o -name '.pnpm-store' \) -print)
  if [[ -n "$junk" ]]; then
    echo "$junk"
    fail "junk/build/cache files found"
  else
    pass "no junk/build/cache files found"
  fi
fi

if command -v rg >/dev/null 2>&1; then
  old_brand=$(rg -n --hidden --glob '!**/.git/**' --glob '!**/node_modules/**' --glob '!**/dist/**' --glob '!**/target/**' '新星慧享|shopro|JeecgBoot|yudao-ui-admin|api-dashboard\.yudao|static-vue3\.yudao|test\.yudao' "$ROOT" || true)
  if [[ -n "$old_brand" ]]; then
    echo "$old_brand"
    fail "old brand/business residue found"
  else
    pass "no old brand/business residue found"
  fi

  removed_modules=$(rg -n --hidden --glob '!**/.git/**' --glob '!**/node_modules/**' --glob '!**/dist/**' --glob '!**/target/**' '/mall/|/trade/|/pay/|/bpm/|/crm/|/erp/|/iot/|(^|[^A-Za-z0-9_])(mall_|trade_|pay_|bpm_|crm_|erp_|iot_)' "$ROOT/muchen-server" "$ROOT/muchen-admin-front/src" "$ROOT/muchen-app" 2>/dev/null || true)
  if [[ -n "$removed_modules" ]]; then
    echo "$removed_modules"
    warn "removed module keywords found; review whether these are allowed references"
  else
    pass "no removed module keyword references found"
  fi
else
  warn "rg not installed; skipped residue scans"
fi

if command -v curl >/dev/null 2>&1; then
  if curl -fsS --max-time 2 "http://localhost:48080/actuator/health" >/dev/null 2>&1; then
    pass "backend health endpoint reachable"
  else
    warn "backend health endpoint not reachable on localhost:48080"
  fi

  if curl -fsSI --max-time 2 "http://localhost:80" >/dev/null 2>&1; then
    pass "admin frontend reachable on localhost:80"
  else
    warn "admin frontend not reachable on localhost:80"
  fi

  if curl -fsSI --max-time 2 "http://localhost:3000" >/dev/null 2>&1; then
    pass "H5 frontend reachable on localhost:3000"
  else
    warn "H5 frontend not reachable on localhost:3000"
  fi
fi

echo "Audit complete: ${ERRORS} error(s), ${WARNINGS} warning(s)."

if [[ "$ERRORS" -gt 0 ]]; then
  exit 1
fi
