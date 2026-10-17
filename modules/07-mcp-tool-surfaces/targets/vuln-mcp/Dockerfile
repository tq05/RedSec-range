# Build context = repo root:  docker build -f modules/07-mcp-tool-surfaces/targets/vuln-mcp/Dockerfile -t ghcr.io/redsec-range/m07-vuln-mcp:latest .
# This target is PRIVILEGED (the run_diagnostic tool shells out -> RCE challenge).
# The application is weak on purpose; the container still runs non-root with no
# capabilities, and the chart forbids egress. Keep it in an isolated ns.
#
# Note: `ping` is intentionally NOT installed. run_diagnostic runs via a shell, so
# the command-injection payload (`; cat ...`) fires regardless of whether the base
# `ping` command exists. Staying registry-only (no apt) lets this image build
# anywhere without a Debian mirror.
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29" \
    "httpx>=0.27" "pydantic>=2.5"
COPY redsec/__init__.py /app/redsec/__init__.py
COPY redsec/mockllm/ /app/redsec/mockllm/
COPY modules/07-mcp-tool-surfaces/targets/vuln-mcp/app.py /app/app.py
# The app plants its lab files under /app at startup, so the unprivileged user owns
# it. RCE through run_diagnostic then lands as uid 10001, not root.
RUN chown -R 10001:10001 /app
ENV PYTHONPATH=/app
USER 10001
EXPOSE 9070
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9070"]
