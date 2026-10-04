#!/usr/bin/env bash
# Run every module's challenges against the LIVE kind cluster and verify them.
# For each module it port-forwards the target Services to localhost, runs the
# reference exploit + verifier (reusing the same harness as the Docker runner),
# and reports pass/fail. Run after ./scripts/kind-up.sh.
#
#   ./scripts/kind-run-all.sh [module ...]
set -euo pipefail

CLUSTER="${CLUSTER:-redsec}"
NS_PREFIX="${REDSEC_NS_PREFIX:-redsec}"
MODULES="${*:-01 02 03 04 05 06 07 08 09 11}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
kubectl config use-context "kind-${CLUSTER}" >/dev/null

PF_PIDS=()
cleanup() { for p in "${PF_PIDS[@]:-}"; do kill "$p" 2>/dev/null || true; done; }
trap cleanup EXIT

python3 "$ROOT/scripts/kind_run_all.py" --cluster "$CLUSTER" $MODULES
