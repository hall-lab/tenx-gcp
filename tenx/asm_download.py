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
    sys.stdout.write("Sample: {}\n".format(asm.sample_name))
    old_pwd = os.getcwd()
    try:
        # main: _perf _log
        asm_d = asm.directory()
        sys.stdout.write("Assembly directory: {}\n".format(asm_d))
        if not os.path.exists(asm_d):
            os.makedirs(asm_d)
        os.chdir(asm_d)
        rurl = asm.remote_url()
        sys.stdout.write("Assembly remote url: {}\n".format(rurl))

        rurls_to_dl = []
        for bn in ("_perf", "_log"):
            rurls_to_dl.append( os.path.join(rurl, bn) )
        cmd = ["gsutil", "-m", "cp"]
        cmd += rurls_to_dl + ["."]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)

        # outs: report.txt summary.csv
        outs_d = os.path.join(asm_d, "outs")
        if not os.path.exists(outs_d):
                os.makedirs(outs_d)
        os.chdir(outs_d)
        outs_rurl = os.path.join(rurl, "outs")

        rurls_to_dl = []
        for bn in ("report.txt", "summary.csv"):
                rurls_to_dl.append( os.path.join(outs_rurl, bn) )
        cmd = ["gsutil", "-m", "cp"]
        cmd += rurls_to_dl + ["."]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)

        # mkoutput: ALL
        mkoutput_d = os.path.join(asm_d, "mkoutput")
        if not os.path.exists(mkoutput_d):
                os.makedirs(mkoutput_d)
        os.chdir(mkoutput_d)
        mkoutput_rurl = os.path.join(rurl, "mkoutput")

        cmd = ["gsutil", "-m", "rsync", "-r", mkoutput_rurl, "."]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)
    except:
        raise
    finally:
        os.chdir(old_pwd)
    sys.stdout.write("Download assembly ... DONE\n")

#-- asm_download
