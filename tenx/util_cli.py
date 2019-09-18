import click, sys

from tenx import util

# UTIL
# - calculate-compute-metrics
# - verify-upload

@click.group()
def tenx_util_cli():
    """
    Utilities and Helpers
    """
    pass

@click.command()
@click.argument('directory', type=click.Path(exists=True))
def tenx_util_calculate_compute_metrics(directory):
    """
    Calculate the compute metrics for a 10X genomics pipeline run.
    """
    print( report.compute_metrics_basic(util.calculate_compute_metrics(directory)) )
tenx_util_cli.add_command(tenx_util_calculate_compute_metrics, name='calculate-compute-metrics')

@click.command()
@click.argument('local', type=click.Path(exists=True))
@click.argument('remote', type=click.STRING)
@click.option('--ignore', type=click.STRING, required=False, help="Ignore all files staring with this string. Useful for skipping log dirs.")
def tenx_util_verify_upload(local, remote, ignore):
    """
    Check if all files from LOCAL directory are on REMOTE url.
    """
    sys.stderr.write("Local directory: {}\n".format(local))
    sys.stderr.write("Remote URL: {}\n".format(remote))
    util.verify_upload(ldir=local, rurl=remote, ignore=ignore)
    sys.stderr.write("All local files found on remote!\n")
tenx_util_cli.add_command(tenx_util_verify_upload, name='verify-upload')

#-- UTIL
