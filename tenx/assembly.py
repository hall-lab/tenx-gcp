import glob, os, subprocess, sys, tempfile
from app import TenxApp

class TenxAssembly():

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'assembly')

    def sample_directory(self):
        return os.path.join(TenxApp.config['TENX_DATA_PATH'], self.sample_name)

    def directory(self):
        return os.path.join(self.sample_directory(), 'assembly')

    def outs_assembly_directory(self):
        return os.path.join(self.directory(), 'outs', 'assembly')

    def reads_directory(self):
        return os.path.join(self.sample_directory(), 'reads')

    def mkoutput_directory(self):
        return os.path.join(self.directory(), 'mkoutput')

    def is_successful(self): # TODO make more robust
        return os.path.exists(self.outs_assembly_directory())

#-- TenxAssembly

def assemble_script(asm):
    return """#!/bin/bash
set -e
source /apps/supernova/sourceme.bash
mkdir -p {TENX_SAMPLE_DIRECTORY}
cd {TENX_SAMPLE_DIRECTORY}
supernova run --id=assembly --fastqs={TENX_RDS_DIRECTORY} --uiport=18080 --nodebugmem --localcores=50 --localmem=400
""".format(TENX_SAMPLE_DIRECTORY=asm.sample_directory(), TENX_RDS_DIRECTORY=asm.reads_directory())

def run_assemble(asm):
   script = assemble_script(asm)
   script_f = tempfile.NamedTemporaryFile()
   script_f.write(script)
   script_f.flush()
   rv = subprocess.call(['bash', script_f.name])
   if rv != 0: raise Exception("Failed to run 'assemble' bash script.")
   if not asm.is_successful(): raise Exception("Ran supernova script, but {} was not found!".format(asm.outs_assembly_directory()))

#-- assemble

def mkoutput_script(asm):
    return """#!/bin/bash
set -e
source /apps/supernova/sourceme.bash
echo Running mkoutput...
echo Entering {TENX_ASM_MKOUTPUT_PATH}
mkdir -p {TENX_ASM_MKOUTPUT_PATH}
cd {TENX_ASM_MKOUTPUT_PATH}
echo Running mkoutput raw...
supernova mkoutput --asmdir={TENX_ASM_OUTS_ASSEMBLY_DIRECTORY} --outprefix={TENX_SAMPLE}.raw --style=raw
echo Running mkoutput megabubbles...
supernova mkoutput --asmdir={TENX_ASM_OUTS_ASSEMBLY_DIRECTORY} --outprefix={TENX_SAMPLE}.megabubbles --style=megabubbles
echo Running mkoutput pseudohap2...
supernova mkoutput --asmdir={TENX_ASM_OUTS_ASSEMBLY_DIRECTORY} --outprefix={TENX_SAMPLE}.pseudohap2 --style=pseudohap2
echo Running mkoutput...OK
""".format(TENX_ASM_PATH=asm.directory(), TENX_SAMPLE=asm.sample_name, TENX_ASM_MKOUTPUT_PATH=asm.mkoutput_directory(), TENX_ASM_OUTS_ASSEMBLY_DIRECTORY=asm.outs_assembly_directory())

def run_mkoutput(asm):
   script = mkoutput_script(asm)
   script_f = tempfile.NamedTemporaryFile()
   script_f.write(script)
   script_f.flush()
   print(script)
   rv = subprocess.call(['bash', script_f.name])
   if rv != 0: raise Exception("Failed to run 'mkoutput' bash script.")
   fastas = glob.glob( os.path.join(asm.mkoutput_directory(), '*fasta.gz') )
   if len(fastas) != 4: raise Exception("Expected 4 assembly fasta.gz files in {} after running mkoutput, but only found {}.".format(asm.mkoutput_directory(), len(fastas)))

#-- mkoutput

def run_upload(asm):
    sys.stderr.write("Upload {} assembly...".format(asm.sample_name))

    if not asm.is_successful(): raise Exception("Refusing to upload an unsuccessful assembly!")

    sys.stderr.write("Entering {} ...".format(asm.directory))
    os.chdir(asm.directory())
    if os.path.exists("ASSEMBLER_CS"):
        sys.stderr.write("Removing logging directory ASSEMBLER_CS prior to upload.\n")
        os.rmtree("ASSEMBLER_CS")

    sys.stderr.write("Uploading to: {}".format(asm.remote_url()))
    subprocess.call(["gsutil", "-m", "rsync", "-r", ".", asm.remote_url()])

    # TODO verify

    sys.stderr.write("Upload assembly...OK")

#-- run_upload
