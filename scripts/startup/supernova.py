#!/usr/bin/env python

import glob, os, shutil, requests, subprocess, time

APPS_DIR = '/apps'
DATA_DIR = '@DATA_DIR@'
REMOTE_DATA_URL = '@REMOTE_DATA_URL@'
SUPERNOVA_VERSION = '@SUPERNOVA_VERSION@'

TENX_ETC_DIRECTORY = os.path.join(os.path.sep, "etc", "tenx")
TENX_CONFIG_FILE = os.path.join(TENX_ETC_DIRECTORY, "config.yaml")

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
        'python-pip',
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

    subprocess.call(['pip', 'uninstall', '--yes', 'crcmod']) # ignore rv
    while subprocess.call(['pip', 'install', '-U', 'crcmod']):
        print "Failed to install crcmod. Trying again 5 seconds."
        time.sleep(5)

    while subprocess.call(['timedatectl', 'set-timezone', 'America/Chicago']):
        print "Failed to set timezone with timedatectl. Trying again 5 seconds."
        time.sleep(5)

    subprocess.call(['sed', '-i', 's/^\[Plugin/#[Plugin/', '/etc/boto.cfg'])
    subprocess.call(['sed', '-i', 's/^plugin_/#plugin_/' '/etc/boto.cfg'])

#-- install_packages

def create_data_directory_structures():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        os.chmod(DATA_DIR, 0777)

    if not os.path.exists( os.path.join(APPS_DIR, 'tenx-scripts') ):
        os.makedirs( os.path.join(APPS_DIR, 'tenx-scripts') )

    if not os.path.exists(TENX_ETC_DIRECTORY):
        os.makedirs(TENX_ETC_DIRECTORY)

#-- create_data_directory_structures

def install_supernova():
    if os.path.exists( os.path.join(APPS_DIR, "supernova") ):
        print "Already installed supernova...SKIPPING"
        return

    print "Install supernova..."
    os.chdir(APPS_DIR)
    supernova_bn = '-'.join(['supernova', SUPERNOVA_VERSION])
    supernova_tgz = '.'.join([supernova_bn, "tgz"])
    supernova_url = os.path.join(REMOTE_DATA_URL, "software", supernova_tgz)

    print "Download supernova from " + supernova_url
    subprocess.call(['gsutil', 'ls', '-l', supernova_url]) # check if exists
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
    if os.path.exists( os.path.join(APPS_DIR, "tenx-scripts", "tenxrc") ):
        print "Already installed tenx-scripts...SKIPPING"
        return
    print "Installing tenx-scripts..."

    os.chdir('/tmp')
    subprocess.call(['git', 'clone', 'https://github.com/hall-lab/tenx-gcp.git'])
    os.chdir('tenx-gcp')

    for subdir in ( 'common', 'supernova' ):
        for fn in glob.glob( os.path.join('scripts', subdir, "*") ):
            if os.path.basename(fn).endswith("bats"): continue
            dest_fn = os.path.join(APPS_DIR, 'tenx-scripts', os.path.basename(fn))
            shutil.copy(fn, dest_fn)
            os.chmod(dest_fn, 0777)

    while subprocess.call(['curl', '-H', 'Metadata-Flavor:Google', 
       'http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenxrc',
       '-o', os.path.join(APPS_DIR, 'tenx-scripts', 'tenxrc')]):
        print "Failed curl tenxrc! Trying again in 5 seconds..."
        time.sleep (5)

    os.chdir('/tmp')
    shutil.rmtree('tenx-gcp')
    print "Installing tenx-scripts...OK"

#-- install_tenx_scripts

def add_supernova_profile():
    fn = os.path.join(os.path.sep, "etc", "profile.d", "supernova.sh")
    if os.path.exists(fn):
        print("Already added {} ...SKIPPING".format(fn))
        return

    print "Adding {} ...".format(fn)
    with open(fn, "w") as f:
        f.write("TENX_CONFIG_FILE=" + TENX_CONFIG_FILE + "\n")
        f.write('PATH=/apps/tenx-scripts:"${PATH}"' + "\n")
        f.write("source /apps/supernova/sourceme.bash\n")

#-- add_supernova_profile

def add_tenx_config_file():
    if os.path.exists(TENX_CONFIG_FILE):
        print("Already added tenx config at {}...SKIPPING".format(TENX_CONFIG_FILE))
        return

    print "Adding {} ...".format(TENX_CONFIG_FILE)
    url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenx-config"
    print("GET {}".format(url))
    response = requests.get(url, headers={ "Metadata-Flavor": "Google" })
    if not response.ok: raise Exception("GET failed for {}".format(url))
    with open(TENX_CONFIG_FILE, "w") as f:
        f.write(response.content)

#-- add_tenx_config_file

if __name__ == '__main__':
    install_packages()
    create_data_directory_structures()
    install_supernova()
    install_tenx_scripts()
    add_supernova_profile()
    add_tenx_config_file()
    print "Startup script...DONE"
#-- __main__
