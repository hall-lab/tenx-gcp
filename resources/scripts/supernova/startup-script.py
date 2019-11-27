#!/usr/bin/env python

import glob, os, shutil, stat, sys, re, requests, subprocess, time

APPS_DIR = '/apps'
DATA_DIR =  os.path.join(os.path.sep, "mnt", "disks", "data")
REMOTE_DATA_URL = '@REMOTE_DATA_URL@'
SUPERNOVA_SOFTWARE_URL = '@SUPERNOVA_SOFTWARE_URL@'

TENX_ETC_DIRECTORY = os.path.join(os.path.sep, "etc", "tenx")
TENX_CONFIG_FILE = os.path.join(TENX_ETC_DIRECTORY, "config.yaml")

def start_motd():
    msg = """
***    SUPERNOVA AND TENX IS CURRENTLY BEING INSTALLED/CONFIGURED IN THE BACKGROUND   ***
***                 A TERMINAL BROADCAST WILL ANNOUNCE WHEN COMPLETE                  ***
*** IF THIS MESSAGE PERSISTS FOR AN UNEXPECTED AMOUNT OF TIME, CONTACT YOUR SYS ADMIN ***
"""
    f = open('/etc/motd', 'w')
    f.write(msg)
    f.close()

#-- start_motd()

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
        'python3',
        'redhat-rpm-config',
	'sssd-client',
	'sudo',
	'which',
	'unzip',
	'vim',
        ]
    cmd = ['yum', 'install', '-y'] + packages
    print("RUNNING: {}".format(cmd))
    while subprocess.call(cmd):
        print("yum failed to install packages. Trying again in 5 seconds")
        time.sleep(5)

    # Python deps
    cmd = ["pip", "install", "--upgrade", "pyyaml", "setuptools"]
    print("RUNNING: {}".format(cmd))
    subprocess.check_call(cmd)
    cmd = ["pip3", "install", "--upgrade", "setuptools", "wheel"]
    print("RUNNING: {}".format(cmd))
    subprocess.check_call(cmd)

    # CRC
    cmd = ["pip", "uninstall", "--yes", "crcmod"]
    print("RUNNING: {}".format(cmd))
    subprocess.call(cmd)

    cmd = ["pip", "install", "-U", "crcmod"]
    print("RUNNING: {}".format(cmd))
    rv = subprocess.check_call(cmd)

    # Timezone
    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    print("RUNNING: {}".format(cmd))
    rv = subprocess.check_call(cmd)

    # BOTO CFG - cannot have plugin defined
    subprocess.call(['sed', '-i', 's/^\[Plugin/#[Plugin/', '/etc/boto.cfg'])
    subprocess.call(['sed', '-i', 's/^plugin_/#plugin_/', '/etc/boto.cfg'])

#-- install_packages

def create_data_directory_structures():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        os.chmod(DATA_DIR, stat.S_IRWXU)
        os.chmod(DATA_DIR, stat.S_IRWXG)
        os.chmod(DATA_DIR, stat.S_IRWXO)

    if not os.path.exists( os.path.join(APPS_DIR, 'tenx-scripts') ):
        os.makedirs( os.path.join(APPS_DIR, 'tenx-scripts') )

    if not os.path.exists(TENX_ETC_DIRECTORY):
        os.makedirs(TENX_ETC_DIRECTORY)

#-- create_data_directory_structures

def install_supernova():
    if os.path.exists( os.path.join(APPS_DIR, "supernova") ):
        print("Already installed supernova...SKIPPING")
        return

    print("Install supernova...")
    os.chdir(APPS_DIR)

    print("Download supernova from " + SUPERNOVA_SOFTWARE_URL)
    subprocess.call(['gsutil', 'ls', '-l', SUPERNOVA_SOFTWARE_URL]) # check if exists
    while subprocess.call(['gsutil', '-m', 'cp', SUPERNOVA_SOFTWARE_URL, '.']):
        print("Failed to download supernova! Trying again in 5 seconds...")
        time.sleep (5)

    supernova_glob = glob.glob("supernova*gz")
    if not len(supernova_glob): raise Exception("Failed to find DL'd supernova tgz!")
    supernova_tgz = supernova_glob[0]
    print("Found supernova TGZ: " + supernova_tgz)

    print("UNTAR supernova...")
    while subprocess.call(['bsdtar', 'zxf', supernova_tgz]):
        print("Failed to untar the supernova tgz! Trying again in 5 seconds...")
        time.sleep (5)

    supernova_dir = re.sub(r'\.t(ar\.)?gz', "", supernova_tgz)
    if not os.path.exists(supernova_dir): raise Exception("Failed to find untarred supnova directory!")
    shutil.move(supernova_dir, 'supernova')
    os.remove(supernova_tgz)
    print("Install supernova...OK")

#-- install_supernova

def install_tenx_cli():

    if os.path.exists( os.path.join(APPS_DIR, "usr", "bin", "tenx") ):
        print("Already installed tenx cli...SKIPPING")
        return
    print("Installing tenx cli...")

    os.chdir('/tmp')
    #rv = subprocess.call(['git', 'clone', 'https://github.com/hall-lab/tenx-gcp.git'])
    rv = subprocess.call(["git", "clone", "--single-branch", "--branch", "python3", "https://github.com/hall-lab/tenx-gcp.git"])
    if rv != 0: raise Exception("Failed to git clone the tenx-gcp repo.")

    os.chdir('tenx-gcp')
    rv = subprocess.call(['pip3', 'install', '.'])
    if rv != 0: raise Exception("Failed to install tenx cli.")

    os.chdir('/tmp')
    shutil.rmtree('tenx-gcp')
    print("Installing tenx-scripts...OK")

#-- install_tenx_cli

def add_supernova_profile():
    fn = os.path.join(os.path.sep, "etc", "profile.d", "supernova.sh")
    if os.path.exists(fn):
        print("Already added {} ...SKIPPING".format(fn))
        return

    print("Adding {} ...".format(fn))
    with open(fn, "w") as f:
        f.write("export TENX_CONFIG_FILE=" + TENX_CONFIG_FILE + "\n")
        f.write('export PATH=/apps/tenx-scripts:"${PATH}"' + "\n")
        f.write("source /apps/supernova/sourceme.bash\n")
        f.write("export LANG=en_US.utf-8\n")
        f.write("export LC_ALL=en_US.utf-8\n")

#-- add_supernova_profile

def add_tenx_config_file():
    if os.path.exists(TENX_CONFIG_FILE):
        print("Already added tenx config at {}...SKIPPING".format(TENX_CONFIG_FILE))
        return
    print("Adding {} ...".format(TENX_CONFIG_FILE))
    import yaml

    url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenx-config"
    print("GET {}".format(url))
    response = requests.get(url, headers={ "Metadata-Flavor": "Google" })
    if not response.ok: raise Exception("GET failed for {}".format(url))
    tenx_conf = yaml.safe_load(response.content)

    machine_type = tenx_conf["TENX_MACHINE_TYPE"].split("-")
    machine_cores = int(machine_type[2])
    machine_mem = int(machine_cores * 6.5) # highmem
    print("Machine cores: {}".format(machine_cores))
    print("Machine mem: {}".format(machine_mem))
    # Hold back 2 cores and 13 GB
    tenx_conf["TENX_ASM_CORES"] = machine_cores - 2
    tenx_conf["TENX_ASM_MEM"] = int(machine_mem - (2 * 6.5))

    with open(TENX_CONFIG_FILE, "w") as f:
        f.write( yaml.dump(tenx_conf) )

#-- add_tenx_config_file

def end_motd():
    f = open('/etc/motd', 'w')
    f.write('')
    f.close()

    msg = """
*** SUPERNOVA AND TENX INSTALLATION COMPLETE ***
***        YOU MAY NEED TO LOG OUT/IN        ***
"""
    subprocess.call(['wall', '-n', msg])

#-- end_motd

if __name__ == '__main__':
    print("Startup script...STARTING")
    start_motd()
    create_data_directory_structures()
    install_packages()
    add_supernova_profile()
    add_tenx_config_file()
    install_supernova()
    install_tenx_cli()
    end_motd()
    print("Startup script...DONE")
#-- __main__
