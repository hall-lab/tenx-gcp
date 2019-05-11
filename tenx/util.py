#!/usr/bin/env python

from datetime import datetime, timedelta
import json, os

def run_duration(run_dir):
    #ASSEMBLER_CS ALIGNER_CS BASIC_CS PHASER_SVCALLER_CS
    pwd = os.getcwd()
    paths = []
    try:
        os.chdir(run_dir)
        paths = filter(lambda f:"_CS" in f, os.listdir("."))
        assert len(paths) == 1, "Failed to find log path ending in '_CS'."
        assert os.path.isdir(paths[0]), "Found path ending in _CS, but it is not a directory!"
    finally:
        if len(paths) == 0: os.chdir(pwd)

    log = {
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

                log['jobs'] += 1
                log['duration'] += timedelta(seconds=data['wallclock']['duration_seconds'])
                log['mem'] += data['memGB']
                log['threads'] += data['threads']
                log['core_hours'] += (data['wallclock']['duration_seconds']/3600) * data['threads']

    log['core_hours'] = round(log['core_hours'], 0)
    return log

#-- run_duration
