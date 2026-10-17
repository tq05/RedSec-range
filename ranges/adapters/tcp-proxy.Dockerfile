FROM python:3.14-alpine@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72

RUN addgroup -S redsec && adduser -S redsec -G redsec
COPY ranges/adapters/tcp_proxy.py /opt/redsec/tcp_proxy.py
USER redsec

ENTRYPOINT ["python", "/opt/redsec/tcp_proxy.py"]
