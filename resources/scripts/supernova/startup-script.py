#!/usr/bin/python3

import glob, importlib, os, pip, shutil, re, stat, sys, subprocess, tempfile, time

APPS_DIR = '/apps'
DATA_DIR =  os.path.join(os.path.sep, "mnt", "disks", "data")
SUPERNOVA_SOFTWARE_URL = '@SUPERNOVA_SOFTWARE_URL@'

TENX_ETC_DIR = os.path.join(os.path.sep, "etc", "tenx")
TENX_CONFIG_FILE = os.path.join(TENX_ETC_DIR, "config.yaml")
tenx_conf = None

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
	'ca-certificates',
        'gcc',
        'git',
        'java',
	'make',
	'openssl',
	'openssl-devel',
        'python3-devel',
        'python3-setuptools',
        'redhat-rpm-config',
	'sssd-client',
	'sudo',
        'tmux',
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
    pip.main(["install", "--prefix=/usr", "pyyaml", "requests>=2.20.0"])

    # CRC
    pip.main(["uninstall", "--yes", "crcmod"])
    pip.main(["install", "--prefix=/usr", "--no-cache-dir", "-U", "crcmod"])

    # Timezone
    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    print("RUNNING: {}".format(cmd))
    rv = subprocess.check_call(cmd)

#-- install_packages

def create_data_directory_structures():
    for dn in APPS_DIR, DATA_DIR, TENX_ETC_DIR:
        if not os.path.exists(dn):
            os.makedirs(dn)
    os.chmod(DATA_DIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

#-- create_data_directory_structures

def install_supernova():
    print("Install supernova...")
    if os.path.exists( os.path.join(APPS_DIR, "supernova") ):
        print("Already installed supernova...SKIPPING")
        return

    print("Download supernova from " + SUPERNOVA_SOFTWARE_URL)
    cloudsdk_env = { "CLOUDSDK_PYTHON": sys.executable, "CLOUDSDK_GSUTIL_PYTHON": sys.executable }
    subprocess.check_call(['gsutil', 'ls', '-l', SUPERNOVA_SOFTWARE_URL], env=cloudsdk_env) # check if exists
    os.chdir(APPS_DIR)
    subprocess.check_call(['gsutil', '-m', 'cp', SUPERNOVA_SOFTWARE_URL, '.'], env=cloudsdk_env)

    supernova_glob = glob.glob("supernova*gz")
    if not len(supernova_glob):
        raise Exception("Failed to find DL'd supernova tgz!")
    supernova_tgz = supernova_glob[0]
    print("Found supernova TGZ: " + supernova_tgz)

    print("UNTAR supernova...")
    try:
        #subprocess.check_call(['bsdtar', 'zxf', supernova_tgz]):
        subprocess.check_call(['tar', 'zxf', supernova_tgz])
    except:
        print("Failed to untar the supernova tgz!")
        raise

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
    rv = subprocess.call(['git', 'clone', 'https://github.com/hall-lab/tenx-gcp.git'])
    if rv != 0: raise Exception("Failed to git clone the tenx-gcp repo.")

    os.chdir('tenx-gcp')
    rv = subprocess.call(['pip3', 'install', '.'])
    if rv != 0: raise Exception("Failed to install tenx cli.")

    os.chdir('/tmp')
    shutil.rmtree('tenx-gcp')
    print("Installing tenx cli...OK")

#-- install_tenx_cli

def add_supernova_profile():
    fn = os.path.join(os.path.sep, "etc", "profile.d", "supernova.sh")
    if os.path.exists(fn):
        print("Already added {} ...SKIPPING".format(fn))
        return

    print("Adding {} ...".format(fn))
    with open(fn, "w") as f:
        f.write("export TENX_CONFIG_FILE=" + TENX_CONFIG_FILE + "\n")
        f.write("[ -e /apps/supernova/sourceme.bash ] && source /apps/supernova/sourceme.bash\n")
        f.write("export LANG=en_US.utf-8\n")
        f.write("export LC_ALL=en_US.utf-8\n")
        f.write("export CLOUDSDK_PYTHON={}".format(sys.executable))
        f.write("export CLOUDSDK_GSUTIL_PYTHON={}".format(sys.executable))

#-- add_supernova_profile

def add_tenx_config_file():
    if os.path.exists(TENX_CONFIG_FILE):
        print("Already added tenx config at {}...SKIPPING".format(TENX_CONFIG_FILE))
        return
    print("Adding {} ...".format(TENX_CONFIG_FILE))

    import requests, yaml
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

def install_cromwell():
    print("Install cromwell...")
    import requests, yaml
    with open(TENX_CONFIG_FILE, "r") as f:
         tenx_conf = yaml.safe_load(f)
    dn = tenx_conf["TENX_CROMWELL_PATH"]
    jar_fn = os.path.join(dn, ".".join(["cromwell", "jar"]))
    print("Local JAR:  {}".format(jar_fn))
    if os.path.exists(jar_fn):
        print("Already installed at {} ...".format(jar_fn))
        return

    if not os.path.exists(dn):
        os.makedirs(dn)
    cromwell_version = tenx_conf["TENX_CROMWELL_VERSION"]
    print("Version: {}".format(cromwell_version))
    url = "https://github.com/broadinstitute/cromwell/releases/download/{0}/{1}-{0}.jar".format(cromwell_version, "cromwell")
    print("URL: {}".format(url))
    response = requests.get(url)
    if not response.ok: raise Exception("GET failed for {}".format(url))
    print("Writing content to {}".format(jar_fn))
    with open(jar_fn, "wb") as f:
        f.write(response.content)

    print("Install cromwell...DONE")

#-- install_cromwell

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
    install_cromwell()
    end_motd()
    print("Startup script...DONE")

#-- __main__
