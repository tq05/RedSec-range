#!/usr/bin/env bash
# Show Fly Machine and range readiness/status.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=deploy/fly/lib.sh
source "$HERE/lib.sh"
JSON=false
[ "${1:-}" != "--json" ] || { JSON=true; shift; }
[ "$#" -eq 0 ] || die "usage: deploy/fly/status.sh [--json]"
require_fly_auth
APP="$(require_app)"

if [ "$JSON" = true ]; then
  ready=false
  if "$FLY_BIN" ssh console --quiet --app "$APP" \
      --command 'test -f /run/redsec-ready' >/dev/null 2>&1; then
    ready=true
  fi
  printf '{"app":"%s","ready":%s}\n' "$APP" "$ready"
  [ "$ready" = true ]
else
  "$FLY_BIN" status --app "$APP"
  echo
  "$FLY_BIN" ssh console --quiet --app "$APP" \
    --command 'test -f /run/redsec-ready && range status'
fi
