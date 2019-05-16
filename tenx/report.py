import os

def compute_metrics_basic(metrics):
    return """
Directory:  {}
Hours:      {}
Jobs:       {}
Mem:        {}
Threads:    {}
Core Hours: {}""".format(os.path.abspath(metrics['directory']), round((metrics['duration'].total_seconds()/3600), 0), metrics['jobs'],
        metrics['mem'], metrics['threads'], metrics['core_hours'])
