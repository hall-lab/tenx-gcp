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
def aln_cli():
    """
    Commands, Pipeline, and Helpers for Alignments
    """
    pass

@click.command(short_help="align with longranger")
@click.argument('sample-name', type=click.STRING)
@click.argument('ref-name', type=click.STRING)
def aln_align_cmd(sample_name, ref_name):
    """
    Create alignments with longranger.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sample = TenxSample(name=sample_name, base_path=TenxApp.config["TENX_DATA_PATH"])
    ref = TenxReference(name=ref_name)
    aln = sample.alignment(ref=ref)
    alignment.run_align(aln)
aln_cli.add_command(aln_align_cmd, name="align")

from tenx.aln_pipeline import aln_pipeline_cmd
aln_cli.add_command(aln_pipeline_cmd, name="pipeline")

@click.command(short_help="to the cloud")
@click.argument('sample-name', type=click.STRING)
def aln_upload_cmd(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sample = TenxSample(name=sample_name, base_path=TenxApp.config["TENX_DATA_PATH"])
    aln = sample.alignment()
    rsample = TenxSample(name=sample_name, base_path=TenxApp.config["TENX_REMOTE_URL"])
    raln = sample.alignment()
    alignment.run_upload(aln, raln)
aln_cli.add_command(aln_upload_cmd, name="upload")
