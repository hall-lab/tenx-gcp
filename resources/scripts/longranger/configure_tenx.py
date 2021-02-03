#!/usr/bin/python3

import os, requests, sys, yaml
import os, shutil, subprocess, sys

def configure_tenx(TENX_CONFIG_FILE):
    # Timezone
    sys.stderr.write("Setting timezone...\n")
    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    sys.stderr.write(f"RUNNING: {' '.join(cmd)}")
    rv = subprocess.check_call(cmd)

    # TENX_CONFIG_FILE
    sys.stderr.write(f"Adding {TENX_CONFIG_FILE}...\n")
    tenx_config_dn = os.path.dirnam(TENX_CONFIG_FILE)
    if not os.path.exists(tenx_config_dn):
        os.makedirs(tenx_config_dn)
    url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenx-config"
    sys.stderr.write(f"GET {url}")
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
        f.write("export TENX_CONFIG_FILE=/apps/tenx/config.yaml\n")
        f.write("[ -f /apps/longranger/sourceme.bash ] && . /apps/longranger/sourceme.bash\n")
#-- configure_tenx
