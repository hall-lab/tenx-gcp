# Python 3
FROM python:3.7.3-stretch

# File Author / Maintainer
LABEL maintainer="ebelter@wustl.edu"

# Deps
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  ca-certificates \
  curl \
  less \
  libnss-sss \
  gcc \
  man \
  sqlite3 \
  xz-utils \
  vim && \
  apt-get clean

# Install Tenx
WORKDIR /tmp/build/
COPY ./ ./
RUN pip install .
WORKDIR /
RUN rm -rf /tmp/build/

# Environment
ENV TZ=America/Chicago \
  MGI_NO_GAPP=1 \
  LANG=C \
  LSF_SERVERDIR=/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/etc \
  LSF_LIBDIR=/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/lib \
  LSF_BINDIR=/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/bin \
  LSF_ENVDIR=/opt/lsf9/conf \
  PATH="/opt/lsf9/9.1/linux2.6-glibc2.3-x86_64/bin:${PATH}"

WORKDIR /
CMD [/bin/bash, --login]
