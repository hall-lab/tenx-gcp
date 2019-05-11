import os
from app import TenxApp

class TenxAssembly():

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'assembly')

    def local_directory(self):
        return os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], self.sample_name, 'assembly')

#-- TenxAssembly

def mkoutput_script(asm):
    return """source /apps/supernova/sourceme.bash
echo Running mkoutput...
echo Entering {TENX_ASM_PATH}/mkoutput
mkdir -p {TENX_ASM_PATH}/mkoutput
cd {TENX_ASM_PATH}/mkoutput
echo Running mkoutput raw...
supernova mkoutput --asmdir={TENX_ASM_PATH}/outs/assembly --outprefix={TENX_SAMPLE}.raw --style=raw
echo Running mkoutput megabubbles...
supernova mkoutput --asmdir={TENX_ASM_PATH}/outs/assembly --outprefix={TENX_SAMPLE}.megabubbles --style=megabubbles
echo Running mkoutput pseudohap2...
supernova mkoutput --asmdir={TENX_ASM_PATH}/outs/assembly --outprefix={TENX_SAMPLE}.pseudohap2 --style=pseudohap2
echo Running mkoutput...OK
""".format(TENX_ASM_PATH=asm.local_directory(), TENX_SAMPLE=asm.sample_name)

def run_mkoutput(asm):
   script = mkoutput_script_for_assembly(asm)

#-- mkoutput
