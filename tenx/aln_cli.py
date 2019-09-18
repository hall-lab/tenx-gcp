import click, os, socket, sys

import tenx.app as app
from tenx.version import __version__
from tenx import app, alignment, reads, reference, report, util
from alignment import TenxAlignment
from reads import TenxReads
from reference import TenxReference
import notifications

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
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    alignment.run_align(TenxAlignment(sample_name=sample_name), TenxReads(sample_name=sample_name), TenxReference(name=ref_name))
tenx_aln_cli.add_command(aln_align, name="align")

@click.command(short_help="run the full longranger wgs alignment pipeline")
@click.argument('sample-name', type=click.STRING)
@click.argument('ref-name', type=click.STRING)
def aln_pipeline(sample_name, ref_name):
    """
    Fully automated pipeline to create longranger wgs alignments.

    Process includes: downloading reads & reference, running longranger, and then uploading the alignments to the cloud.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    sys.stderr.write("Run longranger wgs pipeline for {}".format(sample_name))
    notifications.slack("{} ALN START {}".format(sample_name, socket.gethostname()))
    try:
        ref = TenxReference(name=ref_name)
        reference.download(ref)
        rds = TenxReads(sample_name=sample_name)
        reads.download(rds)
        aln = alignment.TenxAlignment(sample_name=sample_name)
        alignment.run_align(aln, ref, rds)
        compute_metrics = util.calculate_compute_metrics(aln.directory())
        print( report.compute_metrics_basic(compute_metrics) )
        with open(os.path.join(aln.directory(), "outs", "compute-metrics.txt"), "w") as f:
            f.write( report.compute_metrics_basic(metrics=compute_metrics) )
        alignment.run_upload(aln)
        sys.stderr.write("Run longranger wgs alignment pipeline...OK")
    except BaseException as ex:
        sys.stderr.write("Exception: {}\n".format(ex))
        sys.stderr.write("Exception encountered, sending notifications if configured...\n")
        notifications.slack("{} ALN FAILED {}".format(sample_name, socket.gethostname()))
        raise
    sys.stderr.write("Finished, sending notifications if configured...\n")
    notifications.slack("{} ALN SUCCESS {}".format(sample_name, socket.gethostname()))
tenx_aln_cli.add_command(aln_pipeline, name="pipeline")

@click.command(short_help="to the cloud")
@click.argument('sample-name', type=click.STRING)
def aln_upload(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    alignment.run_upload(alignment.TenxAlignment(sample_name=sample_name))
tenx_aln_cli.add_command(aln_upload, name="upload")

#-- ALIGNMENT
