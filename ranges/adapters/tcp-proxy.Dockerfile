FROM python:3.12-alpine

RUN addgroup -S redsec && adduser -S redsec -G redsec
COPY ranges/adapters/tcp_proxy.py /opt/redsec/tcp_proxy.py
USER redsec

ENTRYPOINT ["python", "/opt/redsec/tcp_proxy.py"]
