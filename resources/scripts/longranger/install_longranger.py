#!/usr/bin/env python

import glob, os, shutil, re, subprocess

APPS_DIR = '/apps'
LONGRANGER_SOFTWARE_URL = '@LONGRANGER_SOFTWARE_URL@'

def install_longranger():
    if os.path.exists( os.path.join(APPS_DIR, "longranger") ):
        print "Already installed longranger...SKIPPING"
        return

    print "Install longranger..."
    os.chdir(APPS_DIR)

    print "Download longranger from " + LONGRANGER_SOFTWARE_URL
    subprocess.call(['gsutil', 'ls', '-l', LONGRANGER_SOFTWARE_URL]) # check if exists
    subprocess.check_call(['gsutil', '-m', 'cp', LONGRANGER_SOFTWARE_URL, '.']):

    longranger_glob = glob.glob("longranger*gz")
    if not len(longranger_glob): raise Exception("Failed to find DL'd longranger tgz!")
    longranger_tgz = longranger_glob[0]
    print "Found longranger TGZ: " + longranger_tgz

    print "UNTAR longranger..."
    subprocess.check_call(['bsdtar', 'zxf', longranger_tgz]):

    longranger_dir = re.sub(r'\.t(ar\.)?gz', "", longranger_tgz)
    if not os.path.exists(longranger_dir): raise Exception("Failed to find untarred supnova directory!")
    shutil.move(longranger_dir, 'longranger')
    os.remove(longranger_tgz)
    print "Install longranger...OK"

#-- install_longranger

if __name__ == '__main__':
    install_longranger()
