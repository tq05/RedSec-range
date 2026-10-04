# Build context = repo root:  docker build -f modules/09-infra-deployment/targets/appserver/Dockerfile -t ghcr.io/redsec-range/m09-appserver:latest .
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29" "httpx>=0.27" "pydantic>=2.5"
COPY modules/09-infra-deployment/targets/appserver/app.py /app/app.py
USER 10001
EXPOSE 9090
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9090"]
