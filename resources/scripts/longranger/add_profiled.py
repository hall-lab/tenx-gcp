#!/usr/bin/python3

import os, shutil, subprocess, sys

def add_profiled():
    fn = os.path.join(os.path.sep, "etc", "profile.d", "longranger.sh")
    if os.path.exists(fn):
        sys.stderr.write("Already added {} ... SKIPPING\n".format(fn))
        return

    sys,stderr.write(f"Adding {fn} ...")
    with open(fn, "w") as f:
        f.write("export TENX_CONFIG_FILE=/apps/tenx/config.yaml\n")
        f.write("[ -f /apps/longranger/sourceme.bash ] && . /apps/longranger/sourceme.bash\n")

#-- add_profiled

if __name__ == '__main__':
    add_profiled()
