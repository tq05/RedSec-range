#!/usr/bin/env bash
# Create a private Fly app, deploy the range, and wait until every target is ready.
set -Eeuo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=deploy/fly/lib.sh
source "$HERE/lib.sh"
cd "$FLY_ROOT"

APP="${FLY_APP:-}"
REGION="${FLY_REGION:-$(state_value region 2>/dev/null || echo lhr)}"
ORG="${FLY_ORG:-}"
TTL="${MAX_RUNTIME_MIN:-0}"
MODULES="${REDSEC_MODULES:-}"
RANGES="${REDSEC_RANGES:-builtin}"
JSON=false
CREATED=false
DEPLOYED=false

usage() {
  cat <<'EOF'
Usage: deploy/fly/up.sh [options]

Options:
  --app NAME       use or create this app (default: saved app or a unique name)
  --region CODE    Fly region (default: lhr)
  --org SLUG       Fly organization
  --ttl MINUTES    stop the Machine after this many minutes (default: 0)
  --modules IDS    start selected modules, e.g. "01 07" (default: all)
  --ranges IDS     enable ranges, e.g. "builtin dvaa mcpgoat" (default: builtin)
  --json           print a machine-readable result on stdout
  -h, --help       show this help

FLY_API_TOKEN can be used instead of an interactive `fly auth login` session.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --app) [ "$#" -ge 2 ] || die "--app requires a value"; APP="$2"; shift 2 ;;
    --region) [ "$#" -ge 2 ] || die "--region requires a value"; REGION="$2"; shift 2 ;;
    --org) [ "$#" -ge 2 ] || die "--org requires a value"; ORG="$2"; shift 2 ;;
    --ttl) [ "$#" -ge 2 ] || die "--ttl requires a value"; TTL="$2"; shift 2 ;;
    --modules) [ "$#" -ge 2 ] || die "--modules requires a value"; MODULES="$2"; shift 2 ;;
    --ranges) [ "$#" -ge 2 ] || die "--ranges requires a value"; RANGES="$2"; shift 2 ;;
    --json) JSON=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

[[ "$TTL" =~ ^[0-9]+$ ]] || die "--ttl must be a non-negative integer"
[[ "$REGION" =~ ^[a-z0-9]+$ ]] || die "invalid Fly region: $REGION"
if [ -n "$MODULES" ]; then
  [[ "$MODULES" =~ ^[0-9][0-9]([[:space:]]+[0-9][0-9])*$ ]] ||
    die "--modules must be space-separated two-digit module IDs"
fi
[[ "$RANGES" =~ ^[a-z0-9][a-z0-9-]*([[:space:]]+[a-z0-9][a-z0-9-]*)*$ ]] ||
  die "--ranges must be space-separated range IDs"

require_fly_auth
APP="${APP:-$(saved_app)}"
APP="${APP:-$(new_app_name)}"
[[ "$APP" =~ ^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$ ]] || die "invalid Fly app name: $APP"

log() { echo ">> $*" >&2; }

cleanup_failed_create() {
  local rc=$?
  if [ "$rc" -ne 0 ] && [ "$CREATED" = true ] && [ "$DEPLOYED" = false ]; then
    log "deployment failed; removing newly-created app $APP"
    "$FLY_BIN" apps destroy "$APP" --yes >/dev/null 2>&1 || true
    clear_state_for "$APP"
  fi
  exit "$rc"
}
trap cleanup_failed_create EXIT

if ! "$FLY_BIN" status --app "$APP" >/dev/null 2>&1; then
  log "creating app $APP"
  create_args=(apps create "$APP" --yes)
  [ -z "$ORG" ] || create_args+=(--org "$ORG")
  "$FLY_BIN" "${create_args[@]}" >&2
  CREATED=true
else
  log "using existing app $APP"
fi
write_state "$APP" "$REGION" "$ORG"

secrets=()
for name in XAI_API_KEY OPENAI_API_KEY REDSEC_LLM_API_KEY; do
  if [ -n "${!name:-}" ]; then
    secrets+=("$name=${!name}")
  fi
done
if [ "${#secrets[@]}" -gt 0 ]; then
  log "staging model API secrets"
  "$FLY_BIN" secrets set --stage --app "$APP" "${secrets[@]}" >&2
fi

log "deploying to $APP in $REGION (the first image build can take several minutes)"
deploy_args=(deploy "$FLY_ROOT" --app "$APP" --config "$HERE/fly.toml"
  --dockerfile "$HERE/Dockerfile" --primary-region "$REGION"
  --ha=false --remote-only --wait-timeout 15m
  --env "MAX_RUNTIME_MIN=$TTL" --env "REDSEC_RANGES=$RANGES")
[ -z "$MODULES" ] || deploy_args+=(--env "REDSEC_MODULES=$MODULES")
"$FLY_BIN" "${deploy_args[@]}" >&2

timeout="${REDSEC_FLY_READY_TIMEOUT:-1200}"
[[ "$timeout" =~ ^[0-9]+$ ]] || die "REDSEC_FLY_READY_TIMEOUT must be an integer"
deadline=$((SECONDS + timeout))
log "waiting for the range readiness check"
until "$FLY_BIN" ssh console --quiet --app "$APP" \
    --command 'test -f /run/redsec-ready && redsec ranges status >/dev/null' \
    >/dev/null 2>&1; do
  if [ "$SECONDS" -ge "$deadline" ]; then
    die "range was not ready after ${timeout}s; inspect with: $FLY_BIN logs --app $APP"
  fi
  sleep 10
done
DEPLOYED=true

if [ "$JSON" = true ]; then
  python3 - "$APP" "$REGION" "$TTL" "$FLY_STATE_FILE" <<'PY'
import json
import sys
print(json.dumps({"app": sys.argv[1], "region": sys.argv[2],
                  "ttl_minutes": int(sys.argv[3]), "ready": True,
                  "state_file": sys.argv[4]}))
PY
else
  cat <<EOF

RedSec Range is ready: $APP

  Interactive SSH:  ./deploy/fly/ssh.sh
  Harness command:  ./deploy/fly/exec.sh range status
  Model assessor:   ./deploy/fly/model.sh 07 --provider grok --model grok-4
  Browser tunnel:   ./deploy/fly/proxy.sh 07
  Destroy it:       ./deploy/fly/down.sh

The app name is saved in .redsec/fly.json, so every helper uses the same range.
EOF
fi
