#!/usr/bin/env python

import glob, os, shutil, re, subprocess, sys, yaml

APPS_DIR = os.path.join(os.path.sep, "apps")

def install_longranger(LONGRANGER_SOFTWARE_URL):
    if os.path.exists( os.path.join(APPS_DIR, "longranger") ):
        sys.stderr.write("Already installed longranger...SKIPPING\n")
        return

    sys.stderr.write("Install longranger...\n")
    sys.stderr.write("Entering {} ...\n".format(APPS_DIR))
    if not os.path.exists(APPS_DIR):
        os.makedirs(APPS_DIR)
    os.chdir(APPS_DIR)

    sys.stderr.write("Download longranger from {}\n".format(LONGRANGER_SOFTWARE_URL))
    subprocess.call(['gsutil', 'ls', '-l', LONGRANGER_SOFTWARE_URL]) # check if exists
    subprocess.check_call(['gsutil', '-m', 'cp', LONGRANGER_SOFTWARE_URL, '.'])

    longranger_glob = glob.glob("longranger*gz")
    if not len(longranger_glob): raise Exception("Failed to find DL'd longranger tgz!")
    longranger_tgz = longranger_glob[0]
    sys.stderr.write("Found longranger TGZ: {}".format(longranger_tgz))

    sys.stderr.write("UNTAR longranger...\n")
    subprocess.check_call(['bsdtar', 'zxf', longranger_tgz])

    longranger_dir = re.sub(r'\.t(ar\.)?gz', "", longranger_tgz)
    if not os.path.exists(longranger_dir): raise Exception("Failed to find untarred supnova directory!")
    shutil.move(longranger_dir, 'longranger')
    os.remove(longranger_tgz)
    sys.stderr.write("Install longranger...OK")

#-- install_longranger

if __name__ == '__main__':
    conf = yaml.safe_load(open( os.path.join(APPS_DIR, "tenx", "config.yaml") ))
    install_longranger(conf['TENX_LONGRANGER_SOFTWARE_URL'])
