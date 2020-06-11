import click, jinja2, json, os, socket, subprocess, sys

from tenx.app import TenxApp, TenxCromwell
import tenx.assembly as assembly
import tenx.asm_upload
import tenx.notifications as notifications
import tenx.reads as reads

@click.command(short_help="run the full supernova assembly pipeline")
@click.argument('sample-name', type=click.STRING)
def asm_pipeline_cmd(sample_name):
    """
    Run the Assembly Pipeline with Cromwell

    Process includes: downloading reads, running supernova, mkoutput, and then uploading the assembly.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sys.stderr.write("Run assembly pipeline for {}\n".format(sample_name))
    hostname = socket.gethostname()
    notifications.slack("{} START {}".format(sample_name, hostname))
    asm = assembly.TenxAssembly(base_path=TenxApp.config["TENX_DATA_PATH"], sample_name=sample_name)
    try:
        run_pipeline(asm)
    except BaseException as ex:
        sys.stderr.write("Exception: {}\n".format(ex))
        sys.stderr.write("Exception encountered, sending notifications if configured...\n")
        notifications.slack("{} FAILED {}".format(sample_name, socket.gethostname()))
        raise
    notifications.slack("{} SUCCESS {}".format(sample_name, hostname))

#-- asm_pipeline_cmd
 
def run_pipeline(asm):
    cromwell = TenxCromwell()
    cmd = cromwell.supernova_command(asm)
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)

#-- run_pipeline
