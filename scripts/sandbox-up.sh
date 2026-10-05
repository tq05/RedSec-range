#!/usr/bin/env bash
# One-shot bootstrap for an interactive, persistent RedSec range inside a
# Docker-capable sandbox (no Kubernetes required). Idempotent: safe to re-run
# after a sandbox idle/reset to restore everything from cold.
#
#   ./scripts/sandbox-up.sh            # ensure dockerd + base image + full range up
#   ./scripts/sandbox-up.sh 03 07      # only these modules
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [ -n "${REDSEC_PYTHON:-}" ]; then
  PYTHON="$REDSEC_PYTHON"
elif [ -x "$ROOT/.venv/bin/python" ]; then
  PYTHON="$ROOT/.venv/bin/python"
else
  PYTHON="$(command -v python3)"
fi

echo "== 1/5 ensure dockerd =="
if ! docker info >/dev/null 2>&1; then
  [ -e /dev/kmsg ] || ln -s /dev/console /dev/kmsg 2>/dev/null || true
  (dockerd --host=unix:///var/run/docker.sock >/var/log/dockerd.log 2>&1 &)
  for _ in $(seq 1 60); do docker info >/dev/null 2>&1 && break; sleep 1; done
fi
docker info >/dev/null 2>&1 && echo "   dockerd up" || { echo "   dockerd FAILED"; exit 1; }

echo "== 2/5 ensure python deps for the controller =="
"$PYTHON" -c "import fastapi, httpx, pydantic, redsec, uvicorn, yaml" 2>/dev/null || \
  "$PYTHON" -m pip install --break-system-packages -q -e .

echo "== 3/5 ensure base image =="
if ! docker images redsec/base:local -q | grep -q .; then
  IMAGE=redsec/base:local bash scripts/build_base_image.sh
fi

echo "== 4/5 install convenience commands (range, grok, assess) =="
WRAPPER_DIR="$(mktemp -d)"
trap 'rm -rf "$WRAPPER_DIR"' EXIT
cat > "$WRAPPER_DIR/range" <<EOF
#!/usr/bin/env bash
exec "$PYTHON" "$ROOT/scripts/range_ctl.py" "\$@"
EOF
cat > "$WRAPPER_DIR/grok" <<EOF
#!/usr/bin/env bash
exec "$PYTHON" "$ROOT/scripts/grok_cli.py" "\$@"
EOF
cat > "$WRAPPER_DIR/assess" <<EOF
#!/usr/bin/env bash
exec "$PYTHON" "$ROOT/scripts/agent_solver.py" "\$@"
EOF
if [ -w /usr/local/bin ]; then
  install -m 0755 "$WRAPPER_DIR"/* /usr/local/bin/
elif command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
  sudo install -m 0755 "$WRAPPER_DIR"/* /usr/local/bin/
else
  mkdir -p "$HOME/.local/bin"
  install -m 0755 "$WRAPPER_DIR"/* "$HOME/.local/bin/"
  export PATH="$HOME/.local/bin:$PATH"
  echo "   add $HOME/.local/bin to PATH in new shells"
fi
echo "   range, grok, assess installed on PATH"

echo "== 5/5 bring the range up =="
"$PYTHON" scripts/range_ctl.py up "$@"
"$PYTHON" scripts/range_ctl.py status
echo
echo "ready."
echo "  range status | range solve <mod> [chal] | range shell <mod> <target>"
echo "  grok \"question\"            # Grok chat   (needs XAI_API_KEY)"
echo "  grok --agent \"do X\"        # Grok agent with shell+http tools in the sandbox"
echo "  assess <mod> --provider grok --model grok-4   # Grok solves the range, verifier-scored"
