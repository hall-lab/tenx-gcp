#!/usr/bin/python3

import os, shutil, subprocess, sys

def install_tenx_cli():

    if os.path.exists( os.path.join(os.path.sep, "usr", "bin", "tenx") ):
        sys.stderr.write("Already installed tenx cli...SKIPPING")
        return
    sys.stderr.write("Installing tenx cli...\n")

    pwd = os.getcwd()
    os.chdir( os.path.join(os.path.sep, "tmp", "tenx-gcp") )
    rv = subprocess.call(["pip3", "install", "."])
    os.chdir(pwd)
    if rv != 0:
        raise Exception("Failed to install tenx cli.")
    sys.stderr.write("Installing tenx cli...OK\n")

#-- install_tenx_cli

if __name__ == '__main__':
    install_tenx_cli()
