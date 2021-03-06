#!/usr/bin/env python

import glob, os, shutil, re, requests, subprocess, sys, time

APPS_DIR = '/apps'
TENX_PATH = os.path.join(APPS_DIR, "tenx")
TENX_CONFIG_FILE = os.path.join(TENX_PATH, "config.yaml")
DATA_DIR =  os.path.join(os.path.sep, "mnt", "disks", "data")
REMOTE_DATA_URL = '@REMOTE_DATA_URL@'
LONGRANGER_SOFTWARE_URL = '@LONGRANGER_SOFTWARE_URL@'

def start_motd():
    msg = """
***    LONGRANGER AND TENX IS CURRENTLY BEING INSTALLED/CONFIGURED IN THE BACKGROUND   ***
***                 A TERMINAL BROADCAST WILL ANNOUNCE WHEN COMPLETE                  ***
*** IF THIS MESSAGE PERSISTS FOR AN UNEXPECTED AMOUNT OF TIME, CONTACT YOUR SYS ADMIN ***
"""
    f = open('/etc/motd', 'w')
    f.write(msg)
    f.close()

#-- start_motd()

def add_longranger_profile():
    fn = os.path.join(os.path.sep, "etc", "profile.d", "longranger.sh")
    if os.path.exists(fn):
        print("Already added {} ...SKIPPING".format(fn))
        return

    print "Adding {} ...".format(fn)
    with open(fn, "w") as f:
        f.write("TENX_CONFIG_FILE={}\n".format(TENX_CONFIG_FILE))
        f.write(". /apps/longranger/sourceme.bash\n")
        #f.write("[ -f /apps/longranger/sourceme.bash ] && . /apps/longranger/sourceme.bash\n")

#-- add_longranger_profile

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
        'screen',
	'sssd-client',
	'sudo',
	'which',
	'unzip',
	'vim',
        ]

    while subprocess.call(['yum', 'install', '-y'] + packages):
        print "Failed to install packages with yum. Trying again in 5 seconds"
        time.sleep(5)

    cmd = ['pip', 'install', '--upgrade', 'google-api-python-client','setuptools']
    rv = subprocess.call(cmd)
    if rv != 0: raise Exception("Failed run: {}".format(' '.join(cmd)))

    subprocess.call(['pip', 'uninstall', '--yes', 'crcmod']) # ignore rv
    rv = subprocess.call(['pip', 'install', '-U', 'crcmod'])
    if rv != 0: raise Exception("Failed run: {}".format(' '.join(cmd)))

    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    rv = subprocess.call(cmd)
    if rv != 0: raise Exception("Failed run: {}".format(' '.join(cmd)))

    subprocess.call(['sed', '-i', 's/^\[Plugin/#[Plugin/', '/etc/boto.cfg'])
    subprocess.call(['sed', '-i', 's/^plugin_/#plugin_/', '/etc/boto.cfg'])

#-- install_packages

def mount_data_disk_and_create_dirs():

    cmds = []
    if not os.path.exists(DATA_DIR):
	os.makedirs(DATA_DIR)
        cmd +=[
            ["mkfs.ext4", "-m", "0", "-F", "-E", "lazy_itable_init=0,discard", "/dev/disk/by-id/scsi-0Google_PersistentDisk_secondary"]
	    ["mount", "-o", "discard,defaults", "/dev/sdb", DATA_DIR],
        ]

    cmds += [
        ["chmod", "0775", DATA_DIR],
        ["chmod", "u+s", DATA_DIR],
        ["chmod", "g+s", DATA_DIR],
        ["chgrp", "-R", "adm", DATA_DIR],
	["mkdir", "-p", os.path.join(DATA_DIR, "references")],
        ["chmod", "0775", os.path.join(DATA_DIR, "references")],
    ]
    for cmd in cmds:
	sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)

    if not os.path.exists(TENX_PATH):
        os.makedirs(TENX_PATH)

#-- mount_data_disk_and_create_dirs

def install_longranger():
    if os.path.exists( os.path.join(APPS_DIR, "longranger") ):
        print "Already installed longranger...SKIPPING"
        return

    print "Install longranger..."
    os.chdir(APPS_DIR)

    print "Download longranger from " + LONGRANGER_SOFTWARE_URL
    subprocess.call(['gsutil', 'ls', '-l', LONGRANGER_SOFTWARE_URL]) # check if exists
    while subprocess.call(['gsutil', '-m', 'cp', LONGRANGER_SOFTWARE_URL, '.']):
        print "Failed to download longranger! Trying again in 5 seconds..."
        time.sleep (5)

    longranger_glob = glob.glob("longranger*gz")
    if not len(longranger_glob): raise Exception("Failed to find DL'd longranger tgz!")
    longranger_tgz = longranger_glob[0]
    print "Found longranger TGZ: " + longranger_tgz

    print "UNTAR longranger..."
    while subprocess.call(['bsdtar', 'zxf', longranger_tgz]):
        print "Failed to untar the longranger tgz! Trying again in 5 seconds..."
        time.sleep (5)

    longranger_dir = re.sub(r'\.t(ar\.)?gz', "", longranger_tgz)
    if not os.path.exists(longranger_dir): raise Exception("Failed to find untarred supnova directory!")
    shutil.move(longranger_dir, 'longranger')
    os.remove(longranger_tgz)
    print "Install longranger...OK"

#-- install_longranger

def install_tenx_cli():

    if os.path.exists( os.path.join(APPS_DIR, "usr", "bin", "tenx") ):
        print "Already installed tenx cli...SKIPPING"
        return
    print "Installing tenx cli..."

    os.chdir('/tmp')
    rv = subprocess.call(['git', 'clone', 'https://github.com/hall-lab/tenx-gcp.git'])
    if rv != 0: raise Exception("Failed to git clone the tenx-gcp repo.")

    os.chdir('tenx-gcp')
    rv = subprocess.call(["pip", "install", "."])
    if rv != 0: raise Exception("Failed to install tenx cli.")

    os.chdir('/tmp')
    shutil.rmtree('tenx-gcp')
    print "Installing tenx cli...OK"

#-- install_tenx_cli

def end_motd():
    f = open('/etc/motd', 'w')
    f.write('')
    f.close()

    msg = """
*** LONGRANGER AND TENX INSTALLATION COMPLETE ***
***        YOU MAY NEED TO LOG OUT/IN        ***
"""
    subprocess.call(['wall', '-n', msg])

#-- end_motd

if __name__ == '__main__':
    print "Startup script...STARTING"
    start_motd()
    mount_data_disk_and_create_dirs()
    add_longranger_profile()
    add_tenx_config_file()
    install_packages()
    install_longranger()
    install_tenx_cli()
    end_motd()
    print "Startup script...DONE"
#-- __main__
