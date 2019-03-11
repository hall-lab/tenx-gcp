#!/bin/bash

set -e

# TZ Central time - Only on CentOS 7+
timedatectl set-timezone 'America/Chicago'

# Install deps
sudo yum install -y \
	bsdtar \
	ca-certificates \
	gcc \
	less \
	make \
	openssl \
	openssl-devel \
    python-devel \
    python-setuptools \
    redhat-rpm-config \
	sssd-client \
	sudo \
	which \
	unzip \
	vim

# CRC
easy_install -U pip
pip uninstall crcmod
pip install -U crcmod

# Install supernova
if [ ! -d /apps/supernova ]; then
    mkdir -p /apps
    cd /apps
	supernova_bn='supernova-@SUPERNOVA_VERSION@'
    supernova_tgz="${supernova_bn}.tgz"
	supernova_source="@REMOTE_DATA_URL@/software/${supernova_tgz}"
	gsutil -m cp "${supernova_source}" .
	bsdtar zxf "${supernova_tgz}"
	rm -f "${supernova_tgz}"
	mv "${supernova_bn}" supernova
fi

# Install run-supernova script
run_supernov='/usr/local/bin/run-supernova'
if [ ! -f "${run_supernova}" ]; then
    curl -H 'Metadata-Flavor:Google' http://metadata.google.internal/computeMetadata/v1/instance/attributes/run-supernova -o "${run_supernova}"
    chmod 0755 "${run_supernova}"
fi
unset run_supernova

# Data location
mkdir -p @DATA_DIR@
chgrp -R adm @DATA_DIR@
chmod -R 775 @DATA_DIR@

# Comment out plugin in the boto config so gsutil will work
sed -i 's/\[Plugin/#[Plugin/' /etc/boto.cfg
sed -i 's/plugin_/#plugin_/' /etc/boto.cfg
