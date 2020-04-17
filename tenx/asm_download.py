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
    remote = assembly.TenxAssembly(sample_name=sample_name, base_path=TenxApp.config["TENX_REMOTE_URL"])
    local = assembly.TenxAssembly(sample_name=sample_name, base_path=TenxApp.config["TENX_DATA_PATH"])
    asm_download(remote, local)

#-- asm_download_cmd

def asm_download(remote, local):
    sys.stdout.write("Download assembly ... \n")
    sys.stdout.write("Remote path: {}\n".format(remote.path))
    sys.stdout.write("Local path: {}\n".format(local.path))
    old_pwd = os.getcwd()
    try:
        if not os.path.exists(local.path):
            os.makedirs(local.path)
        os.chdir(local.path)
        cmd = ["gsutil", "-m", "rsync", "-r", remote.path, "."]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)
    except:
        raise
    finally:
        os.chdir(old_pwd)
    sys.stdout.write("Download assembly ... DONE\n")

#-- asm_download
