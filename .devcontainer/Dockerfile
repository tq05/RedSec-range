FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm@sha256:7876580dc67fd460fd962f004cbeb480027e9bbc0657096f1087db11f9eaff39

# Older cached variants of the upstream image can contain a Yarn apt source whose
# rotated signing key breaks later feature installs. Node is installed by the
# devcontainer feature, so this legacy source is unnecessary.
RUN rm -f /etc/apt/sources.list.d/yarn*.list
