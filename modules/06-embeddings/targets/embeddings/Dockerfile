# Build context = repo root:  docker build -f modules/06-embeddings/targets/embeddings/Dockerfile -t ghcr.io/redsec-range/m06-embeddings:latest .
FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29" "pydantic>=2.5"
COPY modules/06-embeddings/targets/embeddings/app.py /app/app.py
USER 10001
EXPOSE 9060
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9060"]
