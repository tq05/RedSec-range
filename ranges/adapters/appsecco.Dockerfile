FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash python3 python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /lab
COPY . /lab

# Python versions match those available when the cataloged upstream revision shipped.
RUN for directory in /lab/*; do \
      if [ -f "$directory/package-lock.json" ]; then \
        npm ci --omit=dev --no-audit --no-fund --prefix "$directory"; \
      fi; \
    done \
    && python3 -m venv /opt/appsecco-venv \
    && /opt/appsecco-venv/bin/pip install --no-cache-dir \
      mcp==1.24.0 httpx==0.28.1 uvicorn==0.38.0 \
    && mkdir -p /tmp/appsecco-workspace

EXPOSE 3000 8000

CMD ["bash", "-lc", "trap 'kill 0' TERM INT; node /lab/vulnerable-mcp-server-indirect-prompt-injection-remote-mcp/index.js & /opt/appsecco-venv/bin/python /lab/vulnerable-mcp-server-wikipedia-http-streamable/wikipedia-mcp.py & wait -n"]
