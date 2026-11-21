FROM python:3.15-alpine@sha256:0f9552bb28711333da16915ec146f5e6bb44a7fdac9ced15dc17c2e0206346dd

RUN addgroup -S redsec && adduser -S redsec -G redsec
COPY ranges/adapters/tcp_proxy.py /opt/redsec/tcp_proxy.py
USER redsec

ENTRYPOINT ["python", "/opt/redsec/tcp_proxy.py"]
