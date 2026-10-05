FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Older cached variants of the upstream image can contain a Yarn apt source whose
# rotated signing key breaks later feature installs. Node is installed by the
# devcontainer feature, so this legacy source is unnecessary.
RUN rm -f /etc/apt/sources.list.d/yarn*.list
