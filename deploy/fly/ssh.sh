#!/usr/bin/env bash
# Open an interactive shell in the deployed range.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=deploy/fly/lib.sh
source "$HERE/lib.sh"
require_fly_auth
APP="$(require_app)"
exec "$FLY_BIN" ssh console --app "$APP" "$@"
