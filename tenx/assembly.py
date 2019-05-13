import glob, os, subprocess, tempfile
from app import TenxApp

class TenxAssembly():

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'assembly')

    def sample_directory(self):
        return os.path.join(TenxApp.config['TENX_DATA_PATH'], self.sample_name)

    def local_directory(self):
        return os.path.join(self.sample_directory(), 'assembly')

    def reads_directory(self):
        return os.path.join(self.sample_directory(), 'reads')

    def mkoutput_directory(self):
        return os.path.join(self.local_directory(), 'mkoutput')

#-- TenxAssembly

def mkoutput_script(asm):
    return """source /apps/supernova/sourceme.bash
echo Running mkoutput...
echo Entering {TENX_ASM_MKOUTPUT_PATH}
mkdir -p {TENX_ASM_MKOUTPUT_PATH}
cd {TENX_ASM_MKOUTPUT_PATH}
echo Running mkoutput raw...
supernova mkoutput --asmdir={TENX_ASM_PATH}/outs/assembly --outprefix={TENX_SAMPLE}.raw --style=raw
echo Running mkoutput megabubbles...
supernova mkoutput --asmdir={TENX_ASM_PATH}/outs/assembly --outprefix={TENX_SAMPLE}.megabubbles --style=megabubbles
echo Running mkoutput pseudohap2...
supernova mkoutput --asmdir={TENX_ASM_PATH}/outs/assembly --outprefix={TENX_SAMPLE}.pseudohap2 --style=pseudohap2
echo Running mkoutput...OK
""".format(TENX_ASM_PATH=asm.local_directory(), TENX_SAMPLE=asm.sample_name, TENX_ASM_MKOUTPUT_PATH=asm.mkoutput_directory())

def run_mkoutput(asm):
   script = mkoutput_script(asm)
   script_f = tempfile.NamedTemporaryFile()
   script_f.write(script)
   script_f.flush()
   subprocess.call(['bash', script_f.name])
   fastas = glob.glob( os.path.join(asm.mkoutput_directory(), '*fasta.gz') )
   if len(fastas) != 4: raise Exception("Expected 4 assembly fasta.gz files in {} after running mkoutput, but only found {}.".format(asm.mkoutput_directory(), len(fastas)))

#-- mkoutput
