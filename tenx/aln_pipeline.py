import click, socket, subprocess, sys

from tenx.app import TenxApp, TenxCromwell
import tenx.notifications as notifications

from tenx.alignment import TenxAlignment
from tenx.reference import TenxReference
from tenx.sample import TenxSample

@click.command(short_help="run the full longranger wgs alignment pipeline")
@click.argument('sample-name', type=click.STRING)
@click.argument('ref-name', type=click.STRING)
def aln_pipeline_cmd(sample_name, ref_name):
    """
    Fully automated pipeline to create longranger wgs alignments.

    Process includes: downloading reads & reference, running longranger, and then uploading the alignments to the cloud.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sys.stderr.write("Run longranger wgs pipeline for {}".format(sample_name))
    notifications.slack("{} ALN START {}".format(sample_name, socket.gethostname()))
    sample = TenxSample(name=sample_name, base_path=TenxApp.config.get("TENX_DATA_PATH"))
    ref = TenxReference(name=ref_name)
    aln = sample.alignment(ref=ref)
    try:
        run_pipeline(aln)
    except BaseException as ex:
        sys.stderr.write("Exception: {}\n".format(ex))
        sys.stderr.write("Exception encountered, sending notifications if configured...\n")
        notifications.slack("{} ALN FAILED {}".format(sample_name, socket.gethostname()))
        raise
    sys.stderr.write("Run longranger wgs alignment pipeline...OK")
    sys.stderr.write("Finished, sending notifications if configured...\n")
    notifications.slack("{} ALN SUCCESS {}".format(sample_name, socket.gethostname()))
#-- aln_pipeline_cmd
 
def run_pipeline(aln):
    cromwell = TenxCromwell(entity=aln)
    cmd = cromwell.command()
    sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
    subprocess.check_call(cmd)
#-- run_pipeline
