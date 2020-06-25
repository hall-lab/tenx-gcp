import click, os, shutil, subprocess, sys

from tenx.app import TenxApp
import tenx.assembly, tenx.util
from tenx.sample import TenxSample

@click.command(short_help="Send the assembly to the cloud")
@click.argument('sample-name', type=click.STRING)
def asm_upload_cmd(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    local = TenxSample(name=sample_name, base_path=TenxApp.config["TENX_DATA_PATH"]).assembly()
    remote = TenxSample(name=sample_name, base_path=TenxApp.config["TENX_REMOTE_URL"]).assembly()
    run_upload(local, remote)

def run_upload(local, remote):
    sys.stderr.write("Upload {} assembly...\n".format(local.sample.name))

    local_d = local.path
    sys.stderr.write("Local path: {}\n".format(local_d))
    if not os.path.exists(local_d):
        raise Exception("Cannot find local assembly path!")

    if not local.is_successful(): raise Exception("Refusing to upload an unsuccessful assembly!")

    pwd = os.getcwd()
    try:
        sys.stderr.write("Entering {} ...\n".format(local_d))
        os.chdir(local_d)
        if os.path.exists(local.outs_assembly_stats_path): # may have been moved
            sys.stderr.write("Moving the outs / assembly / stats to outs...\n")
            shutil.move(local.outs_assembly_stats_path, local.outs_path)
        sys.stderr.write("Uploading to: {}\n".format(remote.path))
        cmd = ["gsutil", "-m", "rsync", "-r", "-x", "ASSEMBLER_CS/.*|outs/assembly/.*", ".", remote.path]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
    finally:
        os.chdir(pwd)

    sys.stderr.write("Verify upload assembly...\n")
    tenx.util.verify_upload(ldir=local_d, rurl=remote.path, ignore=["ASSEMBLER_CS", "outs/assembly"])

    sys.stderr.write("Upload assembly...OK\n")

#-- run_upload
