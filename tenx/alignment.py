import glob, os, shutil, subprocess, sys, tempfile

from tenx.app import TenxApp
import tenx.util as util

class TenxAlignment():

    def __init__(self, sample, path, ref=None):
        self.sample = sample
        self.path = path
        if ref is not None:
            self.ref = ref
        self.pipeline_path = os.path.join(sample.path, 'pipeline')
        self.outs_path = os.path.join(self.path, 'outs')

    def is_successful(self):
        return os.path.exists( os.path.join(self.outs_path, "summary.csv") )
#-- TenxAlignment

def run_align(aln):
   sys.stderr.write("Creating alignments for {}\n".format(aln.sample.name))
   ref = aln.ref
   if ref is None:
       raise Exception("Need reference set on alignment!")

   sample_d = aln.sample.path
   if not os.path.exists(sample_d):
       os.makedirs(sample_d)
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
       if not os.path.exists(aln.outs_path): raise Exception("Longranger exited 0, but {} does not exist!".format(aln.outs_path))
   except:
       sys.stderr.write("Failed to run longranger!\n")
       raise
   finally:
       os.chdir(pwd)
#-- run_align

def run_upload(aln, remote_aln):
    sys.stderr.write("Upload {} alignment...\n".format(aln.sample.name))

    if not aln.is_successful(): raise Exception("Refusing to upload an unsuccessful alignment!")

    pwd = os.getcwd()
    try:
        sys.stderr.write("Entering {} ...\n".format(aln.path))
        os.chdir(aln.path)
        for cs_subdir in ('ALIGNER_CS', 'PHASER_SVCALLER_CS'):
            if os.path.exists(cs_subdir):
                sys.stderr.write("Removing logging directory {} prior to upload.\n".format(cs_subdir))
                shutil.rmtree(cs_subdir)

        sys.stderr.write("Uploading to: {}\n".format(remote_aln.path))
        subprocess.check_call(["gsutil", "-m", "rsync", "-r", ".", remote_aln.path])

        sys.stderr.write("Verify upload alignment...\n")
        util.verify_upload(ldir=aln.path, rurl=remote_aln.path)
    finally:
        os.chdir(pwd)

    sys.stderr.write("Upload alignment...OK\n")
#-- run_upload
