FROM mcr.microsoft.com/devcontainers/python:3.15-bookworm@sha256:b8311f1315c58c26a06e05fb44fe3f649e1df1ecceb86646d8b9f6a95c94ad07

# Older cached variants of the upstream image can contain a Yarn apt source whose
# rotated signing key breaks later feature installs. Node is installed by the
# devcontainer feature, so this legacy source is unnecessary.
RUN rm -f /etc/apt/sources.list.d/yarn*.list
