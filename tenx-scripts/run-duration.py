#!/usr/binenv python

from datetime import datetime, timedelta
import json
import os

def main():
    #ASSEMBLER_CS ALIGNER_CS BASIC_CS PHASER_SVCALLER_CS
    paths = filter(lambda f:"_CS" in f, os.listdir("."))
    assert len(paths) == 1, "Failed to find log path ending in '_CS'."
    assert os.path.isdir(paths[0]), "Found path ending in _CS, but it is not a directory!"

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
    print """
Hours:      {}
Jobs:       {}
Mem:        {}
Threads:    {}
Core Hours: {}""".format( round((log['duration'].total_seconds()/3600), 0), log['jobs'], log['mem'], log['threads'], log['core_hours'])

# main


if __name__ == '__main__':
    main()
