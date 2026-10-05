#!/usr/bin/env bash
# Destroy the selected Fly app and clear the local deployment state.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=deploy/fly/lib.sh
source "$HERE/lib.sh"

APP=""
JSON=false
while [ "$#" -gt 0 ]; do
  case "$1" in
    --app) [ "$#" -ge 2 ] || die "--app requires a value"; APP="$2"; shift 2 ;;
    --json) JSON=true; shift ;;
    -h|--help) echo "Usage: deploy/fly/down.sh [--app NAME] [--json]"; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

require_fly_auth
APP="$(require_app "$APP")"
echo ">> destroying app $APP" >&2
"$FLY_BIN" apps destroy "$APP" --yes >&2
clear_state_for "$APP"
if [ "$JSON" = true ]; then
  printf '{"app":"%s","destroyed":true}\n' "$APP"
else
  echo "RedSec Range destroyed: $APP"
fi
