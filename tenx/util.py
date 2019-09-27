from datetime import datetime, timedelta
import json, os, re, subprocess, sys

def calculate_compute_metrics(run_dir):
    #ASSEMBLER_CS ALIGNER_CS BASIC_CS PHASER_SVCALLER_CS
    if not os.path.exists(run_dir):
        raise Exception("Cannot compute compute metrics! Run directory {} does not exist!".format(run_dir))
    os.chdir(run_dir)
    paths = []
    paths = filter(lambda f:"_CS" in f, os.listdir("."))
    if not len(paths) == 1:
        raise Exception("Failed to find log path ending in '_CS'.")
    if not os.path.isdir(paths[0]):
        raise Exception("Found path ending in _CS, but it is not a directory!")

    metrics = {
        "directory": run_dir,
        "core_hours": 0,
        "duration": timedelta(0),
        "jobs": 0,
        "mem": 0,
        "threads": 0,
    }
    for root, dirs, fnames in os.walk(paths[0]):
        for fname in fnames:
            if fname == "_jobinfo":
                with open( os.path.join(root, fname) ) as f:
                    data = json.load(f)

                metrics['jobs'] += 1
                metrics['duration'] += timedelta(seconds=data['wallclock']['duration_seconds'])
                metrics['mem'] += data['memGB']
                metrics['threads'] += data['threads']
                metrics['core_hours'] += (data['wallclock']['duration_seconds']/3600) * data['threads']

    metrics['core_hours'] = round(metrics['core_hours'], 0)
    return metrics

#-- calculate_compute_metrics

def verify_upload(ldir, rurl, ignore=None):
    remote = build_remote(rurl)

    if not ldir.endswith('/'): ldir += '/'
    regex = re.compile(r"" + ldir + r"")
    missing = {}
    ldir_file_cnt = 0;
    for root, dirs, files in os.walk(ldir):
        ldir_file_cnt += len(files)
        for f in files:
            fpath = re.sub(regex, '', os.path.join(root, f))
            if not fpath in remote: missing[fpath] = True
            # FIXME check size

    if ldir_file_cnt == 0:
        raise Exception("Local directory does not contain any files!")
    if ignore:
        missing = { k:v for k,v in missing.items() if not k.startswith(ignore) }
    if missing:
        raise Exception("Remote is missing these files:\n{}".format("\n".join(missing.keys())))

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
