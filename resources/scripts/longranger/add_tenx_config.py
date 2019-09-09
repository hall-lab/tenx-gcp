#!/usr/bin/env python

import os, requests, sys

def add_tenx_config_file():
    # /apps/tenx/config.yaml
    tenx_apps_path = os.path.join( os.path.sep, "apps", "tenx")
    if not os.path.exists(tenx_apps_path):
        os.makedirs(tenx_apps_path)

    tenx_config_file = os.path.join(tenx_apps_path, "config.yaml")
    if os.path.exists(tenx_config_file):
        sys.stderr.write("Already added tenx config at {}...SKIPPING\n".format(tenx_config_file))
        return

    sys.stderr.write("Adding {}\n".format(tenx_config_file))
    url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tenx-config"
    sys.stderr.write("GET {}\n".format(url))
    response = requests.get(url, headers={ "Metadata-Flavor": "Google" })
    if not response.ok: raise Exception("GET failed for {}".format(url))
    with open(tenx_config_file, "w") as f:
        f.write(response.content)

#-- add_tenx_config_file

if __name__ == '__main__':
    add_tenx_config_file()
