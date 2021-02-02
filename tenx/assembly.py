import glob, os, shutil, subprocess, sys, tempfile

from tenx.app import TenxApp
import tenx.util as util

class TenxAssembly():

    def __init__(self, sample, path):
        self.sample = sample
        self.path = os.path.join(sample.path, 'assembly')
        self.outs_path = os.path.join(self.path, 'outs')
        self.outs_assembly_path = os.path.join(self.outs_path, 'assembly')
        self.outs_assembly_stats_path = os.path.join(self.outs_assembly_path, 'stats')
        self.assembler_cs_path = os.path.join(self.path, 'ASSEMBLER_CS')
        self.mkoutput_path = os.path.join(self.path, 'mkoutput')

    def is_successful(self): # TODO make more robust
        return os.path.exists(self.outs_assembly_path)

#-- TenxAssembly

def run_assemble(asm):
    cmd = ["supernova", "--help"]
    sys.stderr.write("Checking if supernova is in PATH...\nRUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)

    sample_d = asm.sample.path
    if not os.path.exists(sample_d):
        os.makedirs(sample_d)

    pwd = os.getcwd()
    try:
        os.chdir(sample_d)
        cmd = [
            "supernova", "run", "--id=assembly", "--fastqs={}".format(asm.sample.reads_path), "--uiport=18080", "--nodebugmem",
            "--localcores={}".format(TenxApp.config['TENX_ASM_CORES']), "--localmem={}".format(TenxApp.config['TENX_ASM_MEM']),
        ]
        asm_params = TenxApp.config.get("TENX_ASM_PARAMS", None)
        if asm_params:
            cmd += asm_params.split(" ")
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)
    finally:
        os.chdir(pwd)
    if not asm.is_successful(): raise Exception("Ran supernova script, but {} was not found!".format(asm.outs_assembly_path))

#-- assemble

def run_mkoutput(asm):
    sys.stderr.write("Running mkoutput for {}...\n".format(asm.sample.name))

    if not asm.is_successful(): raise Exception("Assembly is not complete! Cannot run mkoutput!")

    cmd = ["supernova", "--help"]
    sys.stderr.write("Checking if supernova is in PATH...\nRUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)

    mkoutput_d = asm.mkoutput_path
    sys.stderr.write("Entering {}\n".format(mkoutput_d))
    if not os.path.exists(mkoutput_d):
        os.makedirs(mkoutput_d)

    pwd = os.getcwd()
    try:
        os.chdir(mkoutput_d)
        cmd_template = "supernova mkoutput --asmdir={OUTS_ASM_D} --outprefix={SAMPLE_NAME}.{STYLE} --style={STYLE}"
        for style in ("raw", "megabubbles", "pseudohap2"):
            cmd = cmd_template.format(OUTS_ASM_D=asm.outs_assembly_path, SAMPLE_NAME=asm.sample.name, STYLE=style).split(" ")
            sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
            subprocess.check_call(cmd)
        fastas = glob.glob( os.path.join(mkoutput_d, '*fasta.gz') )
    finally:
        os.chdir(pwd)
    if len(fastas) != 4:
        raise Exception("Expected 4 assembly fasta.gz files in {} after running mkoutput, but found {}.".format(asm.mkoutput_path, len(fastas)))

#-- run_mkoutput

def run_cleanup(asm): # remote only
    sys.stderr.write("Cleanup assembly for {} ...\n".format(asm.sample.name))
    sys.stderr.write("Assembly remote URL: {}\n".format(asm.path))

    # check gsutil
    sys.stderr.write("Checking if gsutil is installed...\n")
    cmd = ["which", "gsutil"]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_output(cmd)

    sys.stderr.write("Checking mkfastq files exist.\n")
    cmd = ["gsutil", "ls", os.path.join(asm.mkoutput_path, "*fasta.gz")]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    try:
        out = subprocess.check_output(cmd)
    except:
        raise Exception("Could not find mkoutput fastas!")
    if len(out.decode().split(".fasta.gz\n")) != 5: # 4 files plus blnk after last
        raise Exception("Failed to find 4 mkoutput fasta files. Refusing to remove post assembly files! {}".format(out.decode().split(".fasta.gz")))

    assembler_cs_path = asm.assembler_cs_path
    sys.stderr.write("Removing ASSEMBLER_CS logs path.\n")
    cmd = ["gsutil", "-m", "rm", "-r", assembler_cs_path]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError: # ignore if does not exist
        pass

    # move outs/assembly/stats to outs/
    try:
        outs_assembly_stats_path = asm.outs_assembly_stats_path
        cmd = ["gsutil", "ls", outs_assembly_stats_path]
        rv = subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.stderr.write("Moving outs / assembly / stats to outs.\n")
        outs_path = asm.outs_path
        cmd = ["gsutil", "-m", "mv", outs_assembly_stats_path, outs_path]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError: # ignore if does not exist
        pass
    outs_assembly_path = asm.outs_assembly_path
    sys.stderr.write("Removing outs / assembly path\n")
    cmd = ["gsutil", "-m", "rm", "-r", outs_assembly_path]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sys.stderr.write("Cleanup assembly ... OK\n")

#-- run_cleanup
