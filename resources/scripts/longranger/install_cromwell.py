#!/usr/bin/python3

import requests, yaml

def install_cromwell(tenx_conf):
    print("Install cromwell...")
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

if __name__ == '__main__':
    conf = yaml.safe_load(open( os.path.join(os.path.sep, "apps", "tenx", "config.yaml") ))
    install_longranger(conf)
