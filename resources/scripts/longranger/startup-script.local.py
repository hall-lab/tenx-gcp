#!/usr/bin/python3

import glob, os, pip, re, shutil, subprocess, sys

DATA_DN = os.path.join(os.path.sep, "mnt", "disks", "data")
APPS_DN = os.path.join(os.path.sep, "apps")
TENX_CONFIG_FILE = os.path.join(APPS_DN, "tenx", "config.yaml")
tenx_conf = None
 
def begin_msg():
    msg = """
***    LONGRANGER AND TENX IS CURRENTLY BEING INSTALLED/CONFIGURED IN THE BACKGROUND  ***
***                 A TERMINAL BROADCAST WILL ANNOUNCE WHEN COMPLETE                  ***
*** IF THIS MESSAGE PERSISTS FOR AN UNEXPECTED AMOUNT OF TIME, CONTACT YOUR SYS ADMIN ***
"""
    f = open('/etc/motd', 'w')
    f.write(msg)
    f.close()
#-- begin_msg()

def end_msg():
    f = open('/etc/motd', 'w')
    f.write('')
    f.close()

    msg = """
*** LONGRANGER AND TENX INSTALLATION COMPLETE ***
***        YOU MAY NEED TO LOG OUT/IN        ***
"""
    subprocess.call(['wall', '-n', msg])
#-- end_msg

def configure_data_disk():
    cmds = []
    if not os.path.exists(DATA_DN):
        os.makedirs(DATA_DN)
        cmds +=[
            ["mkfs.ext4", "-m", "0", "-F", "-E", "lazy_itable_init=0,discard", "/dev/disk/by-id/scsi-0Google_PersistentDisk_secondary"],
            ["mount", "-o", "discard,defaults", "/dev/sdb", DATA_DN],
        ]

    cmds += [
        ["chmod", "0777", DATA_DN],
        ["chmod", "u+s", DATA_DN],
        ["chmod", "g+s", DATA_DN],
        ["chgrp", "-R", "adm", DATA_DN],
    ]

    for subdir in ["references"]:
        cmds += [
            ["mkdir", "-p", os.path.join(DATA_DN, subdir)],
            ["chmod", "0777", os.path.join(DATA_DN, subdir)],
        ]

    for cmd in cmds:
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)
#-- configure_data_disk

def configure_tenx():
    import requests, yaml
    # Timezone
    sys.stderr.write("Setting timezone...\n")
    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    sys.stderr.write(f"RUNNING: {' '.join(cmd)}\n")
    rv = subprocess.check_call(cmd)

    # TENX_CONFIG_FILE
    sys.stderr.write(f"Adding {TENX_CONFIG_FILE}...\n")
    tenx_config_dn = os.path.dirname(TENX_CONFIG_FILE)
    if not os.path.exists(tenx_config_dn):
        os.makedirs(tenx_config_dn)
    url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenx-config"
    sys.stderr.write(f"GET {url}\n")
    response = requests.get(url, headers={ "Metadata-Flavor": "Google" })
    if not response.ok:
        raise Exception(f"GET failed for {url}")
    tenx_conf = yaml.safe_load(response.content)
    with open(TENX_CONFIG_FILE, "w") as f:
        f.write( yaml.dump(tenx_conf) )

    # PROFILE.D to set TENX_CONFIG_FILE and source LONGRANGER
    fn = os.path.join(os.path.sep, "etc", "profile.d", "longranger.sh")
    sys.stderr.write(f"Adding {fn} ...\n")
    with open(fn, "w") as f:
        f.write("export TENX_CONFIG_FILE=" + TENX_CONFIG_FILE + "\n")
        f.write("[ -f /apps/longranger/sourceme.bash ] && . /apps/longranger/sourceme.bash\n")
        f.write("export LANG=en_US.utf-8\n")
        f.write("export LC_ALL=en_US.utf-8\n")
        f.write("export CLOUDSDK_PYTHON={}\n".format(sys.executable))
        f.write("export CLOUDSDK_GSUTIL_PYTHON={}\n".format(sys.executable))
    return tenx_conf
#-- configure_tenx

def install_packages():
    sys.stderr.write("Install deps...\n")

    packages = [
        'ca-certificates',
        'git',
        'java',
        'openssl',
        'openssl-devel',
        'python3-devel',
        'python3-setuptools',
        'sssd-client',
        'tmux',
        ]
    cmd = ['yum', 'install', '-y'] + packages
    subprocess.check_call(cmd)

    # Python deps
    sys.stderr.write("Installing python deps...\n")
    pip.main(["install", "--prefix=/usr", "pyyaml", "requests>=2.20.0"])

    # CRC
    pip.main(["uninstall", "--yes", "crcmod"])
    pip.main(["install", "--no-cache-dir", "-U", "crcmod"])
#-- install_packages

def install_longranger():
    if os.path.exists( os.path.join(APPS_DN, "longranger") ):
        sys.stderr.write("Already installed longranger...SKIPPING\n")
        return

    sys.stderr.write("Install longranger...\n")
    sys.stderr.write("Entering {} ...\n".format(APPS_DN))
    if not os.path.exists(APPS_DN):
        os.makedirs(APPS_DN)
    pwd = os.getcwd()
    os.chdir(APPS_DN)

    longranger_url = tenx_conf["TENX_LONGRANGER_SOFTWARE_URL"]
    sys.stderr.write(f"Download longranger from {longranger_url}\n")
    subprocess.call(['gsutil', 'ls', '-l', longranger_url]) # check if exists
    subprocess.check_call(['gsutil', '-m', 'cp', longranger_url, '.'])

    longranger_glob = glob.glob("longranger*gz")
    if not len(longranger_glob):
        raise Exception("Failed to find DL'd longranger tgz!")
    longranger_tgz = longranger_glob[0]
    sys.stderr.write("Found longranger TGZ: {}\n".format(longranger_tgz))

    sys.stderr.write("UNTAR longranger...\n")
    subprocess.check_call(['tar', 'zxf', longranger_tgz])

    longranger_dir = re.sub(r'\.t(ar\.)?gz', "", longranger_tgz)
    if not os.path.exists(longranger_dir):
        raise Exception("Failed to find untarred supnova directory!")
    shutil.move(longranger_dir, 'longranger')
    os.remove(longranger_tgz)
    os.chdir(pwd)
    sys.stderr.write("Install longranger...OK\n")
#-- install_longranger

def install_tenx():
    if os.path.exists( os.path.join(os.path.sep, "usr", "bin", "tenx") ):
        sys.stderr.write("Already installed tenx cli...SKIPPING")
        return
    sys.stderr.write("Installing tenx...\n")

    pwd = os.getcwd()
    tmp_dn = os.path.join(os.path.sep, "tmp")
    os.chdir(tmp_dn)
    cmd = ["git", "clone", "-b", "aln-cromwell", "https://github.com/hall-lab/tenx-gcp.git"]
    #cmd(["git", "clone", "https://github.com/hall-lab/tenx-gcp.git"])
    sys.stderr.write(f"RUNNING: {' '.join(cmd)}\n")
    subprocess.check_call(cmd)

    os.chdir(os.path.join(tmp_dn, "tenx-gcp"))
    rv = subprocess.call(["pip3", "install", "."])
    os.chdir(pwd)
    if rv != 0:
        raise Exception("Failed to install tenx cli.")
    sys.stderr.write("Installing tenx cli...OK\n")
#-- install_tenx

def install_cromwell():
    import requests
    sys.stderr.write("Install cromwell...\n")
    dn = tenx_conf["TENX_CROMWELL_PATH"]
    jar_fn = os.path.join(dn, ".".join(["cromwell", "jar"]))
    sys.stderr.write(f"Local JAR:  {jar_fn}\n")
    if os.path.exists(jar_fn):
        sys.stderr.write(f"Already installed at {jar_fn} ...\n")
        return

    if not os.path.exists(dn):
        os.makedirs(dn)
    cromwell_version = tenx_conf["TENX_CROMWELL_VERSION"]
    sys.stderr.write(f"Version: {cromwell_version}\n")
    url = "https://github.com/broadinstitute/cromwell/releases/download/{0}/{1}-{0}.jar".format(cromwell_version, "cromwell")
    sys.stderr.write(f"URL: {url}\n")
    response = requests.get(url)
    if not response.ok:
        raise Exception("GET failed for {url}")
    sys.stderr.write(f"Writing content to {jar_fn}\n")
    with open(jar_fn, "wb") as f:
        f.write(response.content)
    sys.stderr.write("Install cromwell...DONE\n")
#-- install_cromwell

if __name__ == "__main__":
    sys.stderr.write("Startup script...\n")
   
    begin_msg()
    configure_data_disk()
    install_packages()
    tenx_conf = configure_tenx()
    install_longranger()
    install_tenx()
    install_cromwell()
    end_msg()
    
    sys.stderr.write("Startup script...DONE\n")
#-- __main__
