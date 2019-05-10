#!/usr/bin/env python

import glob, os, subprocess, sys
from app import TenxApp

class TenxReads():

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'reads')

    def local_directory(self):
        return os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], self.sample_name, 'reads')

#-- TenxReads

def download(reads):
    sys.stderr.write("Fetching {0} fastqs from the object store...\n".format(reads.sample_name))

    ldir = reads.local_directory()
    if not os.path.exists(ldir):
        os.makedirs(ldir)

    sys.stderr.write("Entering {0}\n".format(ldir))
    os.chdir(ldir)

    rurl = reads.remote_url()
    sys.stderr.write("Checking for sample reads at {0} ...\n".format(rurl))
    subprocess.check_call(['gsutil',  'ls', rurl])

    subprocess.check_call(['gsutil', '-m', 'rsync', '-r', rurl, '.'])
    fastqs = glob.glob('*fastq*') # TODO use verify upload technology
    if len(fastqs) == 0: raise Exception("Failed to download read fastqs!")

    sys.stderr.write("Fetching fastqs from the object store...OK\n")

#-- download
