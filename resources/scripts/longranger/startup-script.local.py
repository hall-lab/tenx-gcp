#!/usr/bin/python3

import os, shutil, subprocess, sys

sys.stderr.write("Startup script...\n")
tmp_dn = os.path.join(os.path.sep, "tmp")
os.chdir(tmp_dn)
cmd = ["git", "clone", "-b", "aln-cromwell", "https://github.com/hall-lab/tenx-gcp.git"]
#cmd(["git", "clone", "https://github.com/hall-lab/tenx-gcp.git"])
sys.stderr.write(f"RUNNING: {' '.join(cmd)}\n")
subprocess.check_call(cmd)
os.chdir( os.path.join(tmp_dn, "tenx-gcp", "resources", "scripts", "longranger") )

sys.stderr.write("Running install scripts...\n")
DATA_DN = os.path.join(os.path.sep, "mnt", "disks", "data")
APPS_DN = os.path.join(os.path.sep, "apps")
TENX_CONFIG_FILE = os.path.join(APPS_DN, "tenx", "config.yaml")

from update_msgs import begin_msg, end_msg
begin_msg()

from configure_data_disk import configure_data_disk
configure_data_disk(DATA_DN)

from configure_tenx import configure_tenx
configure_tenx(TENX_CONFIG_FILE)

from install_packages import install_packages
install_packages()

import yaml
with open(TENX_CONFIG_FILE, "r") as f:
    conf = yaml.safe_load(f)

from install_longranger import install_longranger
install_longranger(APPS_DIR, conf["TENX_LONGRANGER_SOFTWARE_URL"])

from install_tenx import install_tenx
install_tenx(APPS_DIR, conf[""])

from install_cromwell import install_cromwell
install_tenx(conf)

end_msg()

sys.stderr.write("Removing tenx-gcp git repo...\n")
os.chdir(tmp_dn)
shutil.rmtree("tenx-gcp")
sys.stderr.write("Startup script...DONE\n")
