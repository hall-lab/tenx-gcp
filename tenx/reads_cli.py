import click

from tenx.app import TenxApp
import tenx.reads

# READS
# - download (fetch reads from the cloud)

@click.group(name="reads")
def reads_cli():
    """
    Commands for Reads
    """
    pass

@click.command(short_help="Download reads from the cloud!")
@click.argument('sample-name', type=click.STRING)
def reads_download_cmd(sample_name):
    """
    Download reads from cloud storage to local disk.
    """
    if TenxApp.config is None:
        raise Exception("Must provide tenx yaml config file!")
    tenx.reads.download(tenx.reads.TenxReads(sample_name=sample_name))
reads_cli.add_command(reads_download_cmd, name="download")

#-- READS
