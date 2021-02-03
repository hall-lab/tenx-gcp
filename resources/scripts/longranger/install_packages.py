#!/usr/bin/python3

import subprocess

def install_packages():

    cmd = ['pip', 'install', '--upgrade', 'google-api-python-client', 'requests>=2.20.0', 'setuptools', 'pyyaml']
    rv = subprocess.check_call(cmd)

    subprocess.call(['pip', 'uninstall', '--yes', 'crcmod'])
    cmd = ['pip', 'install', '-U', 'crcmod']
    rv = subprocess.check_call(cmd)

    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    rv = subprocess.check_call(cmd)

    subprocess.call(['sed', '-i', 's/^\[Plugin/#[Plugin/', '/etc/boto.cfg'])
    subprocess.call(['sed', '-i', 's/^plugin_/#plugin_/', '/etc/boto.cfg'])

#-- install_packages

if __name__ == '__main__':
    install_packages()
