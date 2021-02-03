#!/usr/bin/python3

import os, requests, sys, yaml

def install_cromwell(tenx_conf):
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

if __name__ == '__main__':
    conf = yaml.safe_load(open( os.path.join(os.path.sep, "apps", "tenx", "config.yaml") ))
    install_cromwell(conf)
