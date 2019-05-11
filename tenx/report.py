import os

def run_duration_basic(run):
    return """
Directory:  {}
Hours:      {}
Jobs:       {}
Mem:        {}
Threads:    {}
Core Hours: {}""".format(os.path.abspath(run['directory']), round((run['duration'].total_seconds()/3600), 0), run['jobs'],
        run['mem'], run['threads'], run['core_hours'])
