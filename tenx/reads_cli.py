import click

from tenx.app import TenxApp
import tenx.reads, tenx.sample

# READS
# - download (fetch reads from the cloud)

@click.group(name="reads")
def reads_cli():
    """
    Commands for Reads
    """
    pass

#- dl
@click.command(short_help="Download reads from the cloud!")
@click.argument('sample-name', type=click.STRING)
def reads_download_cmd(sample_name):
    """
    Download reads from cloud storage to local disk.
    """
    if TenxApp.config is None:
        raise Exception("Must provide tenx yaml config file!")
    lsample = tenx.sample.TenxSample(base_path=TenxApp.config.get("TENX_DATA_PATH"), name=sample_name)
    rsample = tenx.sample.TenxSample(base_path=TenxApp.config.get("TENX_REMOTE_URL"), name=sample_name)
    tenx.reads.download(lsample, rsample)
reads_cli.add_command(reads_download_cmd, name="download")

#- ul
from tenx.reads_ul import ul_cmd
reads_cli.add_command(ul_cmd, name="ul")
