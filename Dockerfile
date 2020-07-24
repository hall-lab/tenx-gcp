# Python 3
FROM python:3.7.3-stretch

# Maintainer
LABEL maintainer="ebelter@wustl.edu"

# Deps
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  apt-transport-https \
  ca-certificates \
  curl \
  less \
  libnss-sss \
  gcc \
  man \
  python-dev \
  python-setuptools \
  sqlite3 \
  sudo \
  xz-utils \
  vim && \
  apt-get clean

# Install Tenx
WORKDIR /tmp/build/
COPY ./ ./
RUN pip install --upgrade pip \
  && pip install .
WORKDIR /
RUN rm -rf /tmp/build/

# GCP SDK DPKG
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# GCP SDK & Components
RUN sudo apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  kubectl \
  google-cloud-sdk \
  google-cloud-sdk-app-engine-grpc \
  google-cloud-sdk-pubsub-emulator \
  google-cloud-sdk-app-engine-go \
  google-cloud-sdk-datastore-emulator \
  google-cloud-sdk-app-engine-python \
  google-cloud-sdk-cbt \
  google-cloud-sdk-bigtable-emulator \
  google-cloud-sdk-app-engine-python-extras \
  google-cloud-sdk-datalab \
  google-cloud-sdk-app-engine-java

# CRC
RUN easy_install -U pip && \
  pip uninstall --yes crcmod && \
  pip install -U crcmod

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
