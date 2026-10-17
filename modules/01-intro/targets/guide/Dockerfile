# Build context = repo root:  docker build -f modules/01-intro/targets/guide/Dockerfile -t ghcr.io/redsec-range/m01-guide:latest .
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
WORKDIR /app
COPY deploy/constraints.txt /tmp/constraints.txt
RUN pip install --no-cache-dir -c /tmp/constraints.txt "fastapi>=0.110" "uvicorn[standard]>=0.29" "httpx>=0.27" "pydantic>=2.5"
COPY redsec/__init__.py /app/redsec/__init__.py
COPY redsec/mockllm/ /app/redsec/mockllm/
COPY modules/01-intro/targets/guide/app.py /app/app.py
ENV PYTHONPATH=/app
USER 10001
EXPOSE 9010
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9010"]
