import click, os, subprocess, sys

from tenx.app import TenxApp
import tenx.assembly as assembly

@click.command(short_help="download assembly files")
@click.argument('sample-name', type=click.STRING)
def asm_download_cmd(sample_name):
    """
    Download an Assembly
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    asm = assembly.TenxAssembly(sample_name=sample_name)
    asm_download(asm)

#-- asm_download_cmd

def asm_download(asm):
    sys.stdout.write("Download assembly ... \n")
    rurl = asm.remote_url
    sys.stdout.write("Remote path: {}\n".format(rurl))
    asm_d = asm.directory()
    sys.stdout.write("Local path: {}\n".format(asm_d))
    old_pwd = os.getcwd()
    try:
        if not os.path.exists(asm_d):
            os.makedirs(asm_d)
        os.chdir(asm_d)
        cmd = ["gsutil", "-m", "rsync", "-r", rurl, "."]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)
    except:
        raise
    finally:
        os.chdir(old_pwd)
    sys.stdout.write("Download assembly ... DONE\n")

#-- asm_download
