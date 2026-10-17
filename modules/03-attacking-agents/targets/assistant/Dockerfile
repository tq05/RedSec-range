# Build context = repo root:  docker build -f modules/03-attacking-agents/targets/assistant/Dockerfile -t ghcr.io/redsec-range/m03-assistant:latest .
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29" \
    "httpx>=0.27" "pydantic>=2.5"
# Only the deterministic model engine is needed from the framework.
COPY redsec/__init__.py /app/redsec/__init__.py
COPY redsec/mockllm/ /app/redsec/mockllm/
COPY modules/03-attacking-agents/targets/assistant/app.py /app/app.py
ENV PYTHONPATH=/app
USER 10001
EXPOSE 9030
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9030"]
