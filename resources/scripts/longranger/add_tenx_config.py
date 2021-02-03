#!/usr/bin/python3

import os, requests, sys, yaml

def add_tenx_config_file():
    # /apps/tenx/config.yaml
    tenx_apps_path = os.path.join( os.path.sep, "apps", "tenx")
    if not os.path.exists(tenx_apps_path):
        os.makedirs(tenx_apps_path)

    TENX_CONFIG_FILE = os.path.join(tenx_apps_path, "config.yaml")
    if os.path.exists(TENX_CONFIG_FILE):
        sys.stderr.write("Already added tenx config at {}...SKIPPING\n".format(TENX_CONFIG_FILE))
        return

    sys.stderr.write(f"Adding {TENX_CONFIG_FILE}\n")
    url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenx-config"
    print("GET {}".format(url))
    response = requests.get(url, headers={ "Metadata-Flavor": "Google" })
    if not response.ok:
        raise Exception(f"GET failed for {url}")
    tenx_conf = yaml.safe_load(response.content)
    with open(TENX_CONFIG_FILE, "w") as f:
        f.write( yaml.dump(tenx_conf) )

#-- add_tenx_config_file

if __name__ == '__main__':
    add_tenx_config_file()
