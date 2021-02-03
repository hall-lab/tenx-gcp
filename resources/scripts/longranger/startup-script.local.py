#!/usr/bin/python3

import os, shutil, subprocess, sys

def chpath(path):
    sys.stderr.write("Entering {}\n".format(path))
    os.chdir(path)

#-- chpath

def run_cmd(cmd):
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)

#-- run_cmd

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
        'python3-devel',
        'python3-setuptools',
        'redhat-rpm-config',
        'sssd-client',
        'tmux',
        'which',
        'unzip',
        ]

    cmd = ['yum', 'install', '-y'] + packages
    subprocess.check_call(cmd)

    cmd = ['timedatectl', 'set-timezone', 'America/Chicago']
    print("RUNNING: {}".format(cmd))
    rv = subprocess.check_call(cmd)

    subprocess.call(['sed', '-i', 's/^\[Plugin/#[Plugin/', '/etc/boto.cfg'])
    subprocess.call(['sed', '-i', 's/^plugin_/#plugin_/', '/etc/boto.cfg'])

#-- install_packages

if __name__ == '__main__':
    sys.stderr.write("Startup script...\n")

    install_packages()
    chpath( os.path.join(os.path.sep, "tmp") )
    run_cmd(["git", "clone", "-b", "aln-cromwell", "https://github.com/hall-lab/tenx-gcp.git"])
    #run_cmd(["git", "clone", "https://github.com/hall-lab/tenx-gcp.git"])
    chpath( os.path.join(os.path.sep, "tmp", "tenx-gcp", "resources", "scripts", "longranger") )

    sys.stderr.write("Running scripts...\n")
    scripts = [
            "begin_msg.py",
            "configure_data_disk.py",
            "add_profiled.py",
            "add_tenx_config.py",
            "install_longranger.py",
            "install_cromwell.py",
            "install_tenx_cli.py",
            "end_msg.py",
            ]
    for script in scripts:
        run_cmd(["python", script])

    chpath( os.path.join(os.path.sep, "tmp") )
    sys.stderr.write("Removing tenx-gcp git repo...\n")
    shutil.rmtree("tenx-gcp")

    sys.stderr.write("Startup script...DONE\n")
