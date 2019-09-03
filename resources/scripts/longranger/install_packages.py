#!/usr/bin/env python

import subprocess

def install_packages():

    packages = [
        'bsdtar',
	'ca-certificates',
        'gcc',
        'git',
	'less',
	'make',
	'openssl',
	'openssl-devel',
        'python-devel',
        'python-pip',
        'python-setuptool',
        'redhat-rpm-config',
        'screen',
	'sssd-client',
	'sudo',
	'which',
	'unzip',
	'vim',
        ]


    cmd = ['yum', 'install', '-y'] + packages
    subprocess.check_call(cmd)

    cmd = ['pip', 'install', '--upgrade', 'google-api-python-client','setuptools']
    rv = subprocess.check_call(cmd)

    subprocess.call(['pip', 'uninstall', '--yes', 'crcmod']) # ignore rv
    cmd = ['pip', 'install', '-U', 'crcmod']
    rv = subprocess.check_call(cmd)

    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    rv = subprocess.check_call(cmd)

    subprocess.call(['sed', '-i', 's/^\[Plugin/#[Plugin/', '/etc/boto.cfg'])
    subprocess.call(['sed', '-i', 's/^plugin_/#plugin_/', '/etc/boto.cfg'])

#-- install_packages

if __name__ == '__main__':
    install_packages()
