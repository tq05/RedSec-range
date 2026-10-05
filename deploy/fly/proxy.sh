#!/usr/bin/env bash
# Tunnel one private target port to localhost through Fly WireGuard.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=deploy/fly/lib.sh
source "$HERE/lib.sh"

TARGET="${1:-}"
[ -n "$TARGET" ] || die "usage: deploy/fly/proxy.sh MODULE_OR_PORT [LOCAL_PORT]"
case "$TARGET" in
  01) REMOTE=9010 ;; 02) REMOTE=9020 ;; 03) REMOTE=9030 ;;
  04) REMOTE=9040 ;; 05) REMOTE=9050 ;; 06) REMOTE=9060 ;;
  07) REMOTE=9070 ;; 08) REMOTE=9080 ;; 09) REMOTE=9090 ;;
  11) REMOTE=9110 ;; *) REMOTE="$TARGET" ;;
esac
[[ "$REMOTE" =~ ^[0-9]+$ ]] || die "module or numeric port required"
LOCAL="${2:-$REMOTE}"
[[ "$LOCAL" =~ ^[0-9]+$ ]] || die "local port must be numeric"

require_fly_auth
APP="$(require_app)"
echo ">> http://127.0.0.1:$LOCAL -> $APP:$REMOTE (Ctrl-C to stop)" >&2
exec "$FLY_BIN" proxy "$LOCAL:$REMOTE" --app "$APP"
