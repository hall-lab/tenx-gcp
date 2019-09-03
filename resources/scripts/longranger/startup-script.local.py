#!/usr/bin/env python

import os, subprocess, sys

def chpath(path):
    sys.stderr.write("Entering {}\n".format(path))
    os.chdir(path)

def run_cmd(cmd):
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)

#-- run_script

if __name__ == '__main__':
    sys.stderr.write("Startup script...\n")

    run_cmd(["yum", "install", "-y", "git"])
    run_cmd(["pip", "install", "pyyaml"])
    chpath( os.path.join(os.path.sep, "tmp") )
    run_cmd(["git", "clone", "--single-branch", "--branch", "lr-split-scripts", "https://github.com/hall-lab/tenx-gcp.git"])
    chpath( os.path.join(os.path.sep, "tmp", "tenx-gcp", "resources", "scripts", "longranger") )

    sys.stderr.write("Running scripts...\n")
    scripts = [
            "begin_msg.py",
            "configure_data_disk.py",
            "add_profiled.py",
            "add_tenx_config.py",
            "install_packages.py",
            "install_longranger.py",
            "install_tenx_cli.py",
            "end_msg.py",
            ]
    for script in scripts:
        run_cmd(["python", script])

    chpath( os.path.join(os.path.sep, "tmp") )
    sys.stderr.write("Removing tenx-gcp git repo...\n")
    os.rmtree("tenx-gcp")

    print "Startup script...DONE"

#-- __main__
