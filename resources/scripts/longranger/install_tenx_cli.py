#!/usr/bin/env python

import os, shutil, subprocess

def install_tenx_cli():

    if os.path.exists( os.path.join(os.path.sep, "usr", "bin", "tenx") ):
        print "Already installed tenx cli...SKIPPING"
        return
    print "Installing tenx cli..."

    os.chdir('/tmp')
    if not os.path.exists("tenx-gcp"):
        rv = subprocess.call(['git', 'clone', 'https://github.com/hall-lab/tenx-gcp.git'])
        if rv != 0: raise Exception("Failed to git clone the tenx-gcp repo.")

    os.chdir('tenx-gcp')
    rv = subprocess.call(["pip", "install", "."])
    if rv != 0: raise Exception("Failed to install tenx cli.")

    os.chdir('/tmp')
    shutil.rmtree('tenx-gcp')
    print "Installing tenx cli...OK"

#-- install_tenx_cli

if __name__ == '__main__':
    install_tenx_cli()
