import click

from tenx import app, reads
from reads import TenxReads

# READS
# - download (fetch reads from the cloud)

@click.group(name="reads")
def tenx_reads_cli():
    """
    Commands for Reads
    """
    pass

@click.command(short_help="Download reads from the cloud!")
@click.argument('sample-name', type=click.STRING)
def reads_download(sample_name):
    """
    Download reads from cloud storage to local disk.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    reads.download(TenxReads(sample_name=sample_name))
tenx_reads_cli.add_command(reads_download, name="download")

#-- READS
