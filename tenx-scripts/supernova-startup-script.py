#!/usr/bin/env python

import os, shutil, subprocess

APPS_DIR = '/apps'
DATA_DIR = '@DATA_DIR@'
REMOTE_DATA_URL = '@REMOTE_DATA_URL@'
SUPERNOVA_VERSION = '@SUPERNOVA_VERSION@'

def install_packages():

    packages = [
        'bsdtar',
	'ca-certificates',
        'gcc',
        'git',
	'less',
	'make',
	'openssl',
	'openssl-devel',
        'python-devel',
        'python-setuptool',
        'redhat-rpm-config',
	'sssd-client',
	'sudo',
	'which',
	'unzip',
	'vim',
        ]

    while subprocess.call(['yum', 'install', '-y'] + packages):
        print "Failed to install packages with yum. Trying again in 5 seconds"
        time.sleep(5)

    while subprocess.call(['pip', 'install', '--upgrade', 'google-api-python-client']):
        print "Failed to install google python api client. Trying again 5 seconds."

    subprocess.call(['pip', 'uninstall', 'crcmod']) # ignore rv
    while subprocess.call(['pip', 'install', '-U', 'crcmod']):
        print "Failed to install crcmod. Trying again 5 seconds."
        time.sleep(5)

    while subprocess.call(['timedatectl', 'set-timezone', 'America/Chicago']):
        print "Failed to set timezone with timedatectl. Trying again 5 seconds."
        time.sleep(5)

    subprocess.call(['sed', '-i', 's/^\[Plugin/#[Plugin/', '/etc/boto.cfg'])
    subprocess.call(['sed', '-i', 's/^plugin_/#plugin_/' '/etc/boto.cfg'])

#-- install_packages

def install_supernova():
    if os.path.exists(APPS_DIR + "/supernova"): return

    print "Install supernova..."
    os.chdir(APPS_DIR)
    os.mkdir('supernova')
    supernova_bn = 'supernova-@SUPERNOVA_VERSION@'
    supernova_tgz = '.'.join([supernova_bn, "tgz"])
    supernova_url = os.path.join(REMOTE_DATA_URL, "software", supernova_tgz)

    print "Download supernova from " + supernova_url
    while subprocess.call(['gsutil', '-m', 'cp', supernova_url, '.']):
        print "Failed to download supernova! Trying again in 5 seconds..."
        time.sleep (5)

    if not os.path.exists(supernova_tgz): raise Exception("Failed to find DL'd supernova tgz!")
    print "Found supernova TGZ: " + supernova_tgz

    print "UNTAR supernova..."
    while subprocess.call(['bsdtar', 'zxf', supernova_tgz]):
        print "Failed to untar the supernova tgz! Trying again in 5 seconds..."
        time.sleep (5)

    shutil.move(supernova_bn, 'supernova')
    os.remove(supernova_tgz)
    print "Install supernova...OK"

#-- install_supernova

def install_tenx_scripts():
    if os.path.exists(APPS_DIR + "/tenx-scripts"): return
    print "Installing tenx-scripts..."

    os.chdir('/tmp')
    while subprocess.call(['git', 'clone', 'git@github.com:hall-lab/tenx-gcp.git']):
        print "Failed git clone tenx-gcp repo! Trying again in 5 seconds..."
        time.sleep (5)

    shutil.remove('tenx-scripts/tenxrc')    
    while subprocess.call(['curl', '-H', 'Metadata-Flavor:Google', 
       'http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenxrc',
       '-o', 'tenx-scripts/tenxrc']):
        print "Failed curl tenxrc! Trying again in 5 seconds..."
        time.sleep (5)

    shutil.move('tenx-gcp/tenx-scripts', APPS_DIR)
    shutil.rmtree('tenx-gcp/tenx-scripts')
    print "Installing tenx-scripts...OK"

#-- install_tenx_scripts

def create_data_directory_structure():
    mkdir -p DATA_DIR
    chgrp -R adm DATA_DIR
    chmod -R 775 DATA_DIR

#-- create_data_structure

if __name__ == '__main__':
    install_packages()
    install_supernova()
    install_tenx_scripts()
    create_data_directory_structure()

#-- __main__
