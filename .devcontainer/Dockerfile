FROM mcr.microsoft.com/devcontainers/python:3.14-bookworm@sha256:68aef3859e340a2b0cc63260978c5d40e82f48e30fb00503c59cea9104ff8a6b

# Older cached variants of the upstream image can contain a Yarn apt source whose
# rotated signing key breaks later feature installs. Node is installed by the
# devcontainer feature, so this legacy source is unnecessary.
RUN rm -f /etc/apt/sources.list.d/yarn*.list
