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
    alignment.run_align(TenxAlignment(sample_name=sample_name), TenxReference(name=ref_name))
tenx_aln_cli.add_command(aln_align, name="align")

from tenx.aln_pipeline import aln_pipeline_cmd
tenx_aln_cli.add_command(aln_pipeline_cmd, name="pipeline")

@click.command(short_help="to the cloud")
@click.argument('sample-name', type=click.STRING)
def aln_upload(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    alignment.run_upload(alignment.TenxAlignment(sample_name=sample_name))
tenx_aln_cli.add_command(aln_upload, name="upload")
