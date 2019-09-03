#!/usr/bin/env python

import os, subprocess, sys

DATA_DIR = os.path.join( os.path.sep, "mnt", "disks", "data")

def configure_data_disk():

    #conf = yaml.load()

    cmds = []
    if not os.path.exists(DATA_DIR):
	os.makedirs(DATA_DIR)
        cmds +=[
            ["mkfs.ext4", "-m", "0", "-F", "-E", "lazy_itable_init=0,discard", "/dev/disk/by-id/scsi-0Google_PersistentDisk_secondary"]
	    ["mount", "-o", "discard,defaults", "/dev/sdb", DATA_DIR],
        ]

    cmds += [
        ["chmod", "0775", DATA_DIR],
        ["chmod", "u+s", DATA_DIR],
        ["chmod", "g+s", DATA_DIR],
        ["chgrp", "-R", "adm", DATA_DIR],
	["mkdir", "-p", os.path.join(DATA_DIR, "references")],
        ["chmod", "0775", os.path.join(DATA_DIR, "references")],
    ]
    for cmd in cmds:
	sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)

#-- configure_data_disk

if __name__ == '__main__':
    configure_data_disk()
