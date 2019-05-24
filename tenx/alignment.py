import glob, os, shutil, subprocess, sys, tempfile

from app import TenxApp
import util

class TenxAlignment():

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'alignment')

    def sample_directory(self):
        return os.path.join(TenxApp.config['TENX_DATA_PATH'], self.sample_name)

    def directory(self):
        return os.path.join(self.sample_directory(), 'alignment')

    def outs_directory(self):
        return os.path.join(self.directory(), 'outs')

    def reads_directory(self):
        return os.path.join(self.sample_directory(), 'reads')

    def is_successful(self):
        return os.path.exists( os.path.join(self.outs_directory(), "summary.csv") )

#-- TenxAlignment

def run_align(aln, ref, job_params):
   sys.stderr.write("Creating alignments for {}".format(aln.sample_name))

   sample_d = aln.sample_directory()
   os.makedirs(sample_d)
   sys.stderr.write("Entering {}".format(sample_d))
   pwd = os.getcwd()
   os.chdir(sample_d)

   try:
       cmd = ["supernova", "wgs", "--id=alignment",
           "--sample={}".format(aln.sample_name), "--fastqs={}".format(aln.reads_directory()), "--reference={}".format(ref.directory()),
           "--uiport=18080", "--jobmode=".format(job["mode"]), "--localmem={}".format(job.["mem"]), "--localcores={}".format(job["cores"])]
       sys.stderr.write("Running {} ...".format(' '.join(cmd)))
       subprocess.check_call(cmd)
   except:
       sys.stderr.write("Failed to run supernova!")
       raise
   finally:
       os.chdir(pwd)

#-- align

def run_upload(aln):
    sys.stderr.write("Upload {} alignment...\n".format(aln.sample_name))

    if not aln.is_successful(): raise Exception("Refusing to upload an unsuccessful alignment!")

    sys.stderr.write("Entering {} ...\n".format(aln.directory()))
    os.chdir(aln.directory())
    for cs_subdir in ('ALIGNER_CS', 'PHASER_SVCALLER_CS'):
        if os.path.exists(cs_subdir):
            sys.stderr.write("Removing logging directory {} prior to upload.\n".format(cs_subdir))
            shutil.rmtree(cs_subdir)

    sys.stderr.write("Uploading to: {}\n".format(aln.remote_url()))
    subprocess.call(["gsutil", "-m", "rsync", "-r", ".", aln.remote_url()])

    sys.stderr.write("Verify upload alignment...\n")
    util.verify_upload(ldir=aln.directory(), rurl=aln.remote_url())

    sys.stderr.write("Upload alignment...OK\n")

#-- run_upload
