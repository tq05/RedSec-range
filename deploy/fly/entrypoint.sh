#!/usr/bin/env bash
# PID 1 inside the Fly Machine. Delegates the actual bring-up to the repo's own
# maintained bootstrap (scripts/sandbox-up.sh), which: starts the inner dockerd,
# pip-installs the controller, builds the base image, installs the range/grok/assess
# CLIs on PATH, and brings every module up. We then hold PID 1 so `fly ssh console`
# works, with an optional self-destruct timer.
set -uo pipefail

ROOT=/opt/redsec-range
cd "$ROOT"
: "${MAX_RUNTIME_MIN:=0}"   # 0 = stay up until you destroy it; >0 = halt after N min

log() { echo "[redsec-fly $(date -u +%H:%M:%S)] $*"; }

log "bringing the range up via scripts/sandbox-up.sh ..."
# sandbox-up.sh is idempotent and starts its own dockerd. It builds 14 images on
# first boot, so the first run takes a few minutes.
bash scripts/sandbox-up.sh || log "sandbox-up.sh returned non-zero; shell in to inspect: fly ssh console"

log "range should be up. Drive it over 'fly ssh console':"
log "  range status | range solve <mod> [chal] | range verify <mod>"
log "  assess <mod> --provider grok --model grok-4   (needs XAI_API_KEY secret)"

# Optional self-destruct so a forgotten Machine cleans itself up.
if [ "${MAX_RUNTIME_MIN}" -gt 0 ] 2>/dev/null; then
  ( sleep "$((MAX_RUNTIME_MIN*60))"; log "MAX_RUNTIME_MIN=${MAX_RUNTIME_MIN} reached — halting"; halt -f ) &
  log "self-destruct armed: ${MAX_RUNTIME_MIN} min"
fi

log "idle-holding; destroy with './down.sh' or 'fly apps destroy <app>'."
# Keep PID 1 alive. Prefer tailing the inner dockerd log if present.
if [ -f /var/log/dockerd.log ]; then exec tail -f /var/log/dockerd.log; else exec tail -f /dev/null; fi
