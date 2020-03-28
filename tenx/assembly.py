import glob, os, shutil, subprocess, sys, tempfile

from tenx.app import TenxApp
import tenx.util as util

class TenxAssembly():

    def __init__(self, sample_name):
        self.sample_name = sample_name
        if TenxApp.config.get("TENX_REMOTE_URL", None) is not None:
            self.remote_url = os.path.join(TenxApp.config.get("TENX_REMOTE_URL"), self.sample_name, 'assembly')

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'assembly')

    def sample_directory(self):
        return os.path.join(TenxApp.config['TENX_DATA_PATH'], self.sample_name)

    def directory(self):
        return os.path.join(self.sample_directory(), 'assembly')

    def reads_directory(self):
        return os.path.join(self.sample_directory(), 'reads')

    def outs_path(self, remote=False):
        if not remote:
            return os.path.join(self.directory(), 'outs')
        else:
            return os.path.join(self.remote_url, 'outs')

    def outs_assembly_path(self, remote=False):
        return os.path.join(self.outs_path(remote=remote), 'assembly')

    def outs_assembly_stats_path(self, remote=False):
        return os.path.join(self.outs_assembly_path(remote=remote), 'stats')

    def assembler_cs_path(self, remote=False):
        if not remote:
            return os.path.join(self.directory(), 'ASSEMBLER_CS')
        else:
            return os.path.join(self.remote_url, 'ASSEMBLER_CS')

    def mkoutput_path(self, remote=False):
        if not remote:
            return os.path.join(self.directory(), 'mkoutput')
        else:
            return os.path.join(self.remote_url, 'mkoutput')

    def is_successful(self): # TODO make more robust
        return os.path.exists(self.outs_assembly_path())

#-- TenxAssembly

def run_assemble(asm):
    cmd = ["supernova", "--help"]
    sys.stderr.write("Checking if supernova is in PATH...\nRUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)

    sample_d = asm.sample_directory()
    if not os.path.exists(sample_d):
        os.makedirs(sample_d)

    pwd = os.getcwd()
    try:
        os.chdir(sample_d)
        cmd = [
            "supernova", "run", "--id=assembly", "--fastqs={}".format(asm.reads_directory()), "--uiport=18080", "--nodebugmem",
            "--localcores={}".format(TenxApp.config['TENX_ASM_CORES']), "--localmem={}".format(TenxApp.config['TENX_ASM_MEM']),
        ]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)
    finally:
        os.chdir(pwd)
    if not asm.is_successful(): raise Exception("Ran supernova script, but {} was not found!".format(asm.outs_assembly_path()))

#-- assemble

def run_mkoutput(asm):
    sys.stderr.write("Running mkoutput for {}...\n".format(asm.sample_name))

    if not asm.is_successful(): raise Exception("Assembly is not complete! Cannot run mkoutput!")

    cmd = ["supernova", "--help"]
    sys.stderr.write("Checking if supernova is in PATH...\nRUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)

    mkoutput_d = asm.mkoutput_path()
    sys.stderr.write("Entering {}\n".format(mkoutput_d))
    if not os.path.exists(mkoutput_d):
        os.makedirs(mkoutput_d)

    pwd = os.getcwd()
    try:
        os.chdir(mkoutput_d)
        cmd_template = "supernova mkoutput --asmdir={OUTS_ASM_D} --outprefix={SAMPLE_NAME}.{STYLE} --style={STYLE}"
        for style in ("raw", "megabubbles", "pseudohap2"):
            cmd = cmd_template.format(OUTS_ASM_D=asm.outs_assembly_path(), SAMPLE_NAME=asm.sample_name, STYLE=style).split(" ")
            sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
            subprocess.check_call(cmd)
        fastas = glob.glob( os.path.join(asm.mkoutput_path(), '*fasta.gz') )
    finally:
        os.chdir(pwd)
    if len(fastas) != 4:
        raise Exception("Expected 4 assembly fasta.gz files in {} after running mkoutput, but found {}.".format(asm.mkoutput_path(), len(fastas)))

#-- run_mkoutput

def run_cleanup(asm):
    sys.stderr.write("Cleanup assembly for {} ...\n".format(asm.sample_name))
    sys.stderr.write("Assembly remote URL: {}\n".format(asm.remote_url))

    # check gsutil
    sys.stderr.write("Checking if gsutil is installed...\n")
    cmd = ["which", "gsutil"]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_output(cmd)

    # check assembly in correct place
    correct_url = asm.remote_url
    wrong_url = os.path.join(asm.remote_url, asm.sample_name)
    cmd = ["gsutil", "ls", wrong_url]
    rv = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if rv == 0:
        sys.stderr.write("Assembly is incorrect path, will move after cleanup.\n")
        needs_move = True
        asm.remote_url = wrong_url

    sys.stderr.write("Checking mkfastq files exist.\n")
    cmd = ["gsutil", "ls", os.path.join(asm.mkoutput_path(remote=True), "*fasta.gz")]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    try:
        out = subprocess.check_output(cmd)
    except:
        raise Exception("Could not find mkoutput fastas!")
    if len(out.decode().split(".fasta.gz\n")) != 5: # 4 files plus blnk after last
        raise Exception("Failed to find 4 mkoutput fasta files. Refusing to remove post assembly files! {}".format(out.decode().split(".fasta.gz")))

    assembler_cs_path = asm.assembler_cs_path(remote=True)
    sys.stderr.write("Removing ASSEMBLER_CS logs path.\n")
    cmd = ["gsutil", "-m", "rm", "-r", assembler_cs_path]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError: # ignore if does not exist
        pass

    # move outs/assembly/stats to outs/
    try:
        outs_assembly_stats_path = asm.outs_assembly_stats_path(remote=True)
        cmd = ["gsutil", "ls", outs_assembly_stats_path]
        rv = subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.stderr.write("Moving outs / assembly / stats to outs.\n")
        outs_path = asm.outs_path(remote=True)
        cmd = ["gsutil", "-m", "mv", outs_assembly_stats_path, outs_path]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError: # ignore if does not exist
        pass
    outs_assembly_path = asm.outs_assembly_path(remote=True)
    sys.stderr.write("Removing outs / assembly path\n")
    cmd = ["gsutil", "-m", "rm", "-r", outs_assembly_path]
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # move assembly to correct place if needed
    if asm.remote_url == wrong_url:
        sys.stderr.write("Moving assembly to correct path...\n")
        asm.remote_url = correct_url
        sample_url = os.path.join(TenxApp.config['TENX_REMOTE_URL'], asm.sample_name)
        sample_sample_url = os.path.join(sample_url, asm.sample_name)
        cmd = ["gsutil", "-m", "mv", wrong_url, sample_url]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cmd = ["gsutil", "-m", "mv", sample_sample_url, asm.remote_url]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    sys.stderr.write("Cleanup assembly ... OK\n")

#-- run_cleanup

def run_upload(asm):
    sys.stderr.write("Upload {} assembly...\n".format(asm.sample_name))

    asm_d = asm.directory()
    sys.stderr.write("Local path: {}\n".format(asm_d))
    if not os.path.exists(asm_d):
        raise Exception("Cannot find local assembly path!")

    if not asm.is_successful(): raise Exception("Refusing to upload an unsuccessful assembly!")

    pwd = os.getcwd()
    try:
        sys.stderr.write("Entering {} ...\n".format(asm_d))
        os.chdir(asm.directory())
        if os.path.exists(asm.outs_assembly_stats_path()): # may have been moved
            sys.stderr.write("Moving the outs / assembly / stats to outs...\n")
            shutil.move(asm.outs_assembly_stats_path(), asm.outs_path())
        sys.stderr.write("Uploading to: {}\n".format(asm.remote_url))
        cmd = ["gsutil", "-m", "rsync", "-r", "-x", "ASSEMBLER_CS/.*|outs/assembly/.*", ".", asm.remote_url]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
    finally:
        os.chdir(pwd)

    sys.stderr.write("Verify upload assembly...\n")
    util.verify_upload(ldir=asm.directory(), rurl=asm.remote_url, ignore=["ASSEMBLER_CS", "outs/assembly"])

    sys.stderr.write("Upload assembly...OK\n")

#-- run_upload
