#!/usr/bin/env bash
# Shared helpers for the Fly.io lifecycle scripts.

FLY_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLY_ROOT="$(cd "$FLY_HERE/../.." && pwd)"
FLY_STATE_FILE="${REDSEC_FLY_STATE:-$FLY_ROOT/.redsec/fly.json}"

die() {
  echo "error: $*" >&2
  exit 1
}

find_fly() {
  if command -v fly >/dev/null 2>&1; then
    FLY_BIN="$(command -v fly)"
  elif command -v flyctl >/dev/null 2>&1; then
    FLY_BIN="$(command -v flyctl)"
  else
    die "flyctl is required: https://fly.io/docs/flyctl/install/"
  fi
}

require_fly_auth() {
  find_fly
  "$FLY_BIN" auth whoami >/dev/null 2>&1 ||
    die "authenticate with 'fly auth login' or set FLY_API_TOKEN"
}

state_value() {
  local key="$1"
  [ -f "$FLY_STATE_FILE" ] || return 1
  python3 - "$FLY_STATE_FILE" "$key" <<'PY'
import json
import sys

try:
    value = json.load(open(sys.argv[1], encoding="utf-8")).get(sys.argv[2])
except (OSError, ValueError):
    raise SystemExit(1)
if value is None or value == "":
    raise SystemExit(1)
print(value)
PY
}

write_state() {
  local app="$1" region="$2" org="${3:-}"
  mkdir -p "$(dirname "$FLY_STATE_FILE")"
  python3 - "$FLY_STATE_FILE" "$app" "$region" "$org" <<'PY'
import datetime
import json
import os
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = {
    "app": sys.argv[2],
    "region": sys.argv[3],
    "org": sys.argv[4] or None,
    "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
tmp = path.with_suffix(".tmp")
tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
os.replace(tmp, path)
PY
}

clear_state_for() {
  local app="$1" saved=""
  saved="$(state_value app 2>/dev/null || true)"
  if [ "$saved" = "$app" ]; then
    rm -f "$FLY_STATE_FILE"
  fi
}

saved_app() {
  state_value app 2>/dev/null || true
}

require_app() {
  local explicit="${1:-}" app
  app="${explicit:-${FLY_APP:-$(saved_app)}}"
  [ -n "$app" ] ||
    die "no Fly app selected; run deploy/fly/up.sh first or set FLY_APP"
  printf '%s\n' "$app"
}

new_app_name() {
  local suffix
  suffix="$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')"
  printf 'redsec-range-%s-%s\n' "$(date -u +%y%m%d%H%M)" "$suffix"
}
