# Build context = repo root:  docker build -f modules/08-supply-chain/targets/registry/Dockerfile -t ghcr.io/redsec-range/m08-registry:latest .
# PRIVILEGED: /load deserializes untrusted pickle (RCE challenge). Isolated ns only.
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29" "pydantic>=2.5"
COPY modules/08-supply-chain/targets/registry/app.py /app/app.py
# Unpickled payloads run as this unprivileged user, not root.
USER 10001
EXPOSE 9080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9080"]
