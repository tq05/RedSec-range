#!/usr/bin/env bash
# Run one command in the deployed range; intended for Claude/Codex/CI harnesses.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=deploy/fly/lib.sh
source "$HERE/lib.sh"
[ "$#" -gt 0 ] || die "usage: deploy/fly/exec.sh COMMAND [ARG ...]"
require_fly_auth
APP="$(require_app)"

if [ "$#" -eq 1 ]; then
  COMMAND="$1"
else
  COMMAND="$(python3 - "$@" <<'PY'
import shlex
import sys
print(shlex.join(sys.argv[1:]))
PY
)"
fi
exec "$FLY_BIN" ssh console --quiet --app "$APP" --command "$COMMAND"
