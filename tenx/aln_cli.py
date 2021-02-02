import click, os, socket, sys

from tenx.app import TenxApp
import tenx.alignment as alignment
import tenx.notifications as notifications
import tenx.reads as reads
import tenx.reference as reference
import tenx.report as report
import tenx.util as util

from tenx.alignment import TenxAlignment
from tenx.reference import TenxReference
from tenx.sample import TenxSample

# ALIGNMENT
# - align
# - pipeline (dl rds, dl ref, aln, ul aln)
# - upload

@click.group()
def tenx_aln_cli():
    """
    Commands, Pipeline, and Helpers for Alignments
    """
    pass

@click.command(short_help="align with longranger")
@click.argument('sample-name', type=click.STRING)
@click.argument('ref-name', type=click.STRING)
def aln_align(sample_name, ref_name):
    """
    Create alignments with longranger.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sample = TenxSample(name=sample_name, base_path=TenxApp.config['TENX_DATA_PATH'])
    aln = sample.alignment(ref=TenxReference(name=ref_name))
    alignment.run_align(aln)
tenx_aln_cli.add_command(aln_align, name="align")

@click.command(short_help="run the full longranger wgs alignment pipeline")
@click.argument('sample-name', type=click.STRING)
@click.argument('ref-name', type=click.STRING)
def aln_pipeline(sample_name, ref_name):
    """
    Fully automated pipeline to create longranger wgs alignments.

    Process includes: downloading reads & reference, running longranger, and then uploading the alignments to the cloud.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sys.stderr.write("Run longranger wgs pipeline for {}".format(sample_name))
    notifications.slack("{} ALN START {}".format(sample_name, socket.gethostname()))
    try:
        sample = TenxSample(name=sample_name, base_path=TenxApp.config.get("TENX_DATA_PATH"))
        aln = alignment.TenxAlignment(sample=sample, reference=ref)
        rsample = TenxSample(name=sample_name, base_path=TenxApp.config.get("TENX_REMOTE_URL"))
        raln = alignment.TenxAlignment(sample=sample, reference=ref)
        ref = TenxReference(name=ref_name)

        reference.download(ref)
        reads.download(sample, rsample)
        alignment.run_align(aln)
        alignment.run_upload(aln, raln)
    except BaseException as ex:
        sys.stderr.write("Exception: {}\n".format(ex))
        sys.stderr.write("Exception encountered, sending notifications if configured...\n")
        notifications.slack("{} ALN FAILED {}".format(sample_name, socket.gethostname()))
        raise
    sys.stderr.write("Run longranger wgs alignment pipeline...OK")
    sys.stderr.write("Finished, sending notifications if configured...\n")
    notifications.slack("{} ALN SUCCESS {}".format(sample_name, socket.gethostname()))
tenx_aln_cli.add_command(aln_pipeline, name="pipeline")

@click.command(short_help="to the cloud")
@click.argument('sample-name', type=click.STRING)
def aln_upload(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sample = TenxSample(name=sample_name, base_path=TenxApp.config['TENX_DATA_PATH'])
    aln = sample.alignment()
    rsample = TenxSample(name=sample_name, base_path=TenxApp.config['TENX_REMOTE_URL'])
    raln = rsample.alignment()
    alignment.run_upload(aln, raln)
tenx_aln_cli.add_command(aln_upload, name="upload")
