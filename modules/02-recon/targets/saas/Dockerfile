# Build context = repo root:  docker build -f modules/02-recon/targets/saas/Dockerfile -t ghcr.io/redsec-range/m02-saas:latest .
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29"
COPY modules/02-recon/targets/saas/app.py /app/app.py
USER 10001
EXPOSE 9020
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9020"]
