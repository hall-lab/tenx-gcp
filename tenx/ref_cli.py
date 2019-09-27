import click

from tenx import app, reference
from reference import TenxReference

# REFERENCE
@click.group()
def tenx_ref_cli():
    """
    Commands for Reference Sequences
    """
    pass

@click.command(short_help="fetch reference sequences")
@click.argument('ref-name', type=click.STRING)
def ref_download(ref_name):
    """
    Download reference sequences from cloud storage to local disk.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    reference.download(TenxReference(name=ref_name))
tenx_ref_cli.add_command(ref_download, name="download")

#-- REFERENCE