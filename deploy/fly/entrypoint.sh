#!/usr/bin/env bash
# PID 1 inside the Fly Machine: start the range, publish readiness, then hold.
set -euo pipefail

ROOT=/opt/redsec-range
cd "$ROOT"
: "${MAX_RUNTIME_MIN:=0}"
: "${REDSEC_MODULES:=}"

log() { echo "[redsec-fly $(date -u +%H:%M:%S)] $*"; }

[[ "$MAX_RUNTIME_MIN" =~ ^[0-9]+$ ]] || {
  log "MAX_RUNTIME_MIN must be a non-negative integer"
  exit 2
}
rm -f /run/redsec-ready

modules=()
if [ -n "$REDSEC_MODULES" ]; then
  read -r -a modules <<<"$REDSEC_MODULES"
fi

log "starting the range${REDSEC_MODULES:+ (modules: $REDSEC_MODULES)}"
bash scripts/sandbox-up.sh "${modules[@]}"
redsec doctor
range status
touch /run/redsec-ready
log "ready: use range, assess, or grok over Fly SSH"

if [ "$MAX_RUNTIME_MIN" -gt 0 ]; then
  log "Machine will stop after ${MAX_RUNTIME_MIN} minutes; destroy the app with deploy/fly/down.sh"
  sleep "$((MAX_RUNTIME_MIN * 60))"
  log "runtime limit reached; stopping Machine"
  exit 0
fi

log "holding until the Machine is stopped or the app is destroyed"
if [ -f /var/log/dockerd.log ]; then
  tail -F /var/log/dockerd.log &
else
  tail -f /dev/null &
fi
wait "$!"
