#!/usr/bin/env python

import os, re, subprocess, sys

def run(ldir, rurl):

    remote = build_remote(rurl)

    if not ldir.endswith('/'): ldir += '/'
    regex = re.compile(r"" + ldir + r"")
    missing = []
    for root, dirs, files in os.walk(ldir):
        if len(files) == 0: raise Exception("No files found in {}".format(ldir))
        for f in files:
            fpath = re.sub(regex, '', os.path.join(root, f))
            if not fpath in remote: missing.append(fpath)
            # FIXME check size

    if missing:
        raise Exception("Remote is missing these files:\n{}".format("\n".join(missing)))

    sys.stderr.write("All local files found on remote!")

#--verify_upload    

def build_remote(rurl):

    if not rurl.endswith('/'): rurl += '/'
    regex = re.compile(r"" + rurl + r"")
    remote = {}
    out = subprocess.check_output(['gsutil', 'ls', '-l', rurl + '**'])
    for l in out.split("\n"):
        t = l.split() # no arg splits on spaces
        if len(t) == 0: continue # blank line
        replaced = re.sub(regex, '', t[2])
        remote[replaced] = t[0] # file & size
        # FIXME what about TOTAL?
     
    return remote

#-- build_remote

if __name__ == '__main__':
    if len(sys.argv) < 3: raise Exception("Usage: verify_upload.py <LOCAL_DIR> <REMOTE_URL>")
    run(ldir=sys.argv[1], rurl=sys.argv[2])

#-- main
