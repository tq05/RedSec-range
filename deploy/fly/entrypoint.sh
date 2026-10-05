#!/usr/bin/env bash
# PID 1 inside the Fly Machine: start the range, publish readiness, then hold.
set -euo pipefail

ROOT=/opt/redsec-range
cd "$ROOT"
: "${MAX_RUNTIME_MIN:=0}"
: "${REDSEC_MODULES:=}"
: "${REDSEC_RANGES:=builtin}"

log() { echo "[redsec-fly $(date -u +%H:%M:%S)] $*"; }

[[ "$MAX_RUNTIME_MIN" =~ ^[0-9]+$ ]] || {
  log "MAX_RUNTIME_MIN must be a non-negative integer"
  exit 2
}
rm -f /run/redsec-ready

ranges=()
read -r -a ranges <<<"$REDSEC_RANGES"

log "starting ranges: $REDSEC_RANGES${REDSEC_MODULES:+ (built-in modules: $REDSEC_MODULES)}"
redsec ranges enable "${ranges[@]}"
redsec ranges up
redsec doctor
redsec ranges status
touch /run/redsec-ready
log "ready: use redsec ranges, range, assess, or grok over Fly SSH"

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
