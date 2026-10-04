#!/usr/bin/env bash
# One-shot bootstrap for an interactive, persistent RedSec range inside a
# Docker-capable sandbox (no Kubernetes required). Idempotent: safe to re-run
# after a sandbox idle/reset to restore everything from cold.
#
#   ./scripts/sandbox-up.sh            # ensure dockerd + base image + full range up
#   ./scripts/sandbox-up.sh 03 07      # only these modules
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== 1/4 ensure dockerd =="
if ! docker info >/dev/null 2>&1; then
  [ -e /dev/kmsg ] || ln -s /dev/console /dev/kmsg 2>/dev/null || true
  (dockerd --host=unix:///var/run/docker.sock >/var/log/dockerd.log 2>&1 &)
  for i in $(seq 1 20); do docker info >/dev/null 2>&1 && break; sleep 1; done
fi
docker info >/dev/null 2>&1 && echo "   dockerd up" || { echo "   dockerd FAILED"; exit 1; }

echo "== 2/4 ensure python deps for the controller =="
python3 -c "import redsec" 2>/dev/null || pip install --break-system-packages -q -e . 2>/dev/null || true

echo "== 3/4 ensure base image =="
if ! docker images redsec/base:local -q | grep -q .; then
  IMAGE=redsec/base:local bash scripts/build_base_image.sh
fi

echo "== 4/5 install convenience commands (range, grok) =="
cat > /usr/local/bin/range <<EOF
#!/usr/bin/env bash
exec python3 "$ROOT/scripts/range_ctl.py" "\$@"
EOF
cat > /usr/local/bin/grok <<EOF
#!/usr/bin/env bash
exec python3 "$ROOT/scripts/grok_cli.py" "\$@"
EOF
cat > /usr/local/bin/assess <<EOF
#!/usr/bin/env bash
exec python3 "$ROOT/scripts/agent_solver.py" "\$@"
EOF
chmod +x /usr/local/bin/range /usr/local/bin/grok /usr/local/bin/assess
echo "   range, grok, assess installed on PATH"

echo "== 5/5 bring the range up =="
python3 scripts/range_ctl.py up ${*:-} 2>/dev/null || python3 scripts/range_ctl.py up-all
echo
echo "ready."
echo "  range status | range solve <mod> [chal] | range shell <mod> <target>"
echo "  grok \"question\"            # Grok chat   (needs XAI_API_KEY)"
echo "  grok --agent \"do X\"        # Grok agent with shell+http tools in the sandbox"
echo "  assess <mod> --provider grok --model grok-4   # Grok solves the range, verifier-scored"
