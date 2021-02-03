#!/usr/bin/python3

import requests, sys, yaml

def install_cromwell(tenx_conf):
    sys.stderr.write("Install cromwell...")
    dn = tenx_conf["TENX_CROMWELL_PATH"]
    jar_fn = os.path.join(dn, ".".join(["cromwell", "jar"]))
    sys.stderr.write(f"Local JAR:  {jar_fn}")
    if os.path.exists(jar_fn):
        sys.stderr.write(f"Already installed at {jar_fn} ...")
        return

    if not os.path.exists(dn):
        os.makedirs(dn)
    cromwell_version = tenx_conf["TENX_CROMWELL_VERSION"]
    sys.stderr.write(f"Version: {cromwell_version}")
    url = "https://github.com/broadinstitute/cromwell/releases/download/{0}/{1}-{0}.jar".format(cromwell_version, "cromwell")
    sys.stderr.write(f"URL: {}".format(url))
    response = requests.get(url)
    if not response.ok:
        raise Exception("GET failed for {url}")
    sys.stderr.write(f"Writing content to {jar_fn}")
    with open(jar_fn, "wb") as f:
        f.write(response.content)
    sys.stderr.write("Install cromwell...DONE")
#-- install_cromwell

if __name__ == '__main__':
    conf = yaml.safe_load(open( os.path.join(os.path.sep, "apps", "tenx", "config.yaml") ))
    install_longranger(conf)
