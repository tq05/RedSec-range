FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn[standard]>=0.29"
COPY app.py /app/app.py
# Non-root: the sink has no reason to be privileged.
RUN useradd -m app && chown -R app /app
USER app
EXPOSE 9099
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9099"]
