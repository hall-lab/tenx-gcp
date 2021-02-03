#!/usr/bin/python3

import subprocess, sys

def install_packages():
    sys.stderr.write("Install deps...\n")

    packages = [
        'ca-certificates',
        #'gcc',
        #'git',
        #'less',
        #'make',
        'openssl',
        'openssl-devel',
        'python3-devel',
        'python3-setuptools',
        #'redhat-rpm-config',
        'sssd-client',
        'tmux',
        #'unzip',
        ]
    cmd = ['yum', 'install', '-y'] + packages
    subprocess.check_call(cmd)

    # Python deps
    sys.stderr.write("Installing python deps...\n")
    import pip
    pip.main(["install", "--prefix=/usr", "pyyaml", "requests>=2.20.0"])

    # CRC
    pip.main(["uninstall", "--yes", "crcmod"])
    pip.main(["install", "--no-cache-dir", "-U", "crcmod"])
#-- install_packages
