# Build context = repo root:  docker build -f modules/09-infra-deployment/targets/metadata/Dockerfile -t ghcr.io/redsec-range/m09-metadata:latest .
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29"
COPY modules/09-infra-deployment/targets/metadata/app.py /app/app.py
USER 10001
EXPOSE 9091
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9091"]
