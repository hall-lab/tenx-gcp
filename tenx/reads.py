import glob, os, subprocess, sys
from tenx.app import TenxApp

def download(lsample, rsample):
    sys.stderr.write("Fetching {0} fastqs from the object store...\n".format(lsample.name))

    ldir = lsample.reads_path
    if not os.path.exists(ldir):
        os.makedirs(ldir)

    sys.stderr.write("Entering {0}\n".format(ldir))
    os.chdir(ldir)

    rurl = rsample.reads_path
    sys.stderr.write("Checking for sample reads at {0} ...\n".format(rurl))
    subprocess.check_call(['gsutil',  'ls', rurl])

    subprocess.check_call(['gsutil', '-m', 'rsync', '-r', rurl, '.'])
    fastqs = glob.glob('*fastq*') # TODO use verify upload technology
    if len(fastqs) == 0: raise Exception("Failed to download read fastqs!")

    sys.stderr.write("Fetching fastqs from the object store...OK\n")

#-- download
