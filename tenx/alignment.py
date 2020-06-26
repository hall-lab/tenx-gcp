import glob, os, shutil, subprocess, sys, tempfile

from tenx.app import TenxApp
from tenx.sample import TenxSample
import tenx.util as util

class TenxAlignment():

    def __init__(self, sample_name):
        self.sample = TenxSample(name=sample_name, base_path=TenxApp.config.get("TENX_DATA_PATH"))

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample.name, 'alignment')

    def directory(self):
        return os.path.join(self.sample.path, 'alignment')

    def outs_directory(self):
        return os.path.join(self.directory(), 'outs')

    def is_successful(self):
        return os.path.exists( os.path.join(self.outs_directory(), "summary.csv") )

#-- TenxAlignment

def run_align(aln, ref):
   sys.stderr.write("Creating alignments for {}\n".format(aln.sample.name))

   sample_d = aln.sample.path
   if not os.path.exists(sample_d): os.makedirs(sample_d)
   sys.stderr.write("Entering {}\n".format(sample_d))
   pwd = os.getcwd()
   os.chdir(sample_d)

   try:
       cmd = ["longranger", "wgs", "--id=alignment",
           "--sample={}".format(aln.sample.name), "--reference={}".format(ref.directory()), "--fastqs={}".format(aln.sample.reads_path),
            "--vcmode={}".format(TenxApp.config['TENX_ALN_VCMODE']), "--disable-ui", "--jobmode={}".format(TenxApp.config['TENX_ALN_MODE']),
            "--localmem={}".format(TenxApp.config['TENX_ALN_MEM']), "--localcores={}".format(TenxApp.config['TENX_ALN_CORES'])]
       sys.stderr.write("Running {} ...\n".format(' '.join(cmd)))
       subprocess.check_call(cmd)
       if not os.path.exists(aln.outs_directory()): raise Exception("Longranger exited 0, but {} does not exist!".format(aln.outs_directory()))
   except:
       sys.stderr.write("Failed to run longranger!\n")
       raise
   finally:
       os.chdir(pwd)

#-- run_align

def run_upload(aln):
    sys.stderr.write("Upload {} alignment...\n".format(aln.sample.name))

    if not aln.is_successful(): raise Exception("Refusing to upload an unsuccessful alignment!")

    pwd = os.getcwd()
    try:
        sys.stderr.write("Entering {} ...\n".format(aln.directory()))
        os.chdir(aln.directory())
        for cs_subdir in ('ALIGNER_CS', 'PHASER_SVCALLER_CS'):
            if os.path.exists(cs_subdir):
                sys.stderr.write("Removing logging directory {} prior to upload.\n".format(cs_subdir))
                shutil.rmtree(cs_subdir)

        sys.stderr.write("Uploading to: {}\n".format(aln.remote_url()))
        subprocess.check_call(["gsutil", "-m", "rsync", "-r", ".", aln.remote_url()])

        sys.stderr.write("Verify upload alignment...\n")
        util.verify_upload(ldir=aln.directory(), rurl=aln.remote_url())
    finally:
        os.chdir(pwd)

    sys.stderr.write("Upload alignment...OK\n")

#-- run_upload
