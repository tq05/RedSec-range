# Build context = repo root:  docker build -f modules/07-mcp-tool-surfaces/targets/host/Dockerfile -t ghcr.io/redsec-range/m07-host:latest .
FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29" \
    "httpx>=0.27" "pydantic>=2.5"
COPY redsec/__init__.py /app/redsec/__init__.py
COPY redsec/mockllm/ /app/redsec/mockllm/
COPY modules/07-mcp-tool-surfaces/targets/host/app.py /app/app.py
ENV PYTHONPATH=/app
USER 10001
EXPOSE 9071
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9071"]
