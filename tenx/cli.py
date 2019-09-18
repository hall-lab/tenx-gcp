import click, os, socket, sys, tabulate

import tenx.app as app
from tenx.version import __version__
from tenx import app, alignment, assembly, reads, reference, report, util
from alignment import TenxAlignment
from reads import TenxReads
from reference import TenxReference
import notifications
from compute import Job

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """
    10X CLI
    """
    app.TenxApp(os.environ.get('TENX_CONFIG_FILE', None))
    pass

# ALIGNMENT
from aln_cli import tenx_aln_cli
cli.add_command(tenx_aln_cli, name="aln")

# ASSEMBLY
from asm_cli import tenx_asm_cli
cli.add_command(tenx_asm_cli, name="asm")

# COMPUTE
# - list-templates
# - submit
@click.group(name="compute")
def tenx_compute_cmd():
    """
    Commands to work with resources to submit jobs to a compute manager.
    """
    pass

cli.add_command(tenx_compute_cmd)

@click.command(short_help="List available job templates")
def compute_list_templates():
    """
    List compute job templates and details.
    """
    rows = []
    for fn in os.listdir( Job.templates_path() ):
        (name, manager, suffix) = fn.split(".")
        info = Job.load_template_yaml(fn)
        rows += [[ name, manager, " ".join(info["PARAMS"].keys()) ]]
    sys.stdout.write( tabulate.tabulate(rows, ["NAME", "MANAGER", "PARAMS"], tablefmt="simple") )
tenx_compute_cmd.add_command(compute_list_templates, name="list-templates")

@click.command(short_help="Submit a job to a compute cluster")
@click.argument('template', type=click.STRING)
@click.argument('manager', type=click.STRING)
@click.option('--params', type=click.STRING, required=True, help="Parameters for the job template as comma separated key=value pairs. Ex: SAMPLE_NAME=mysample,REF_NAME=grc38")
def compute_submit(template, manager, params):
    """
    Submit a job template to a compute manager with specified parameters.

    See `list-template` sub-command for availble job templates and their params.
    """
    job = Job(name=template, manager=manager)
    sys.stderr.write("Template: {}\nManager: {}\n".format(template, manager))
    job.launch_script(params)
tenx_compute_cmd.add_command(compute_submit, name="submit")

# -- COMPUTE

# READS
# - download (fetch reads from the cloud)
@click.group(name="reads")
def tenx_reads_cmd():
    """
    Commands for Reads
    """
    pass

cli.add_command(tenx_reads_cmd)

@click.command(short_help="Download reads from the cloud!")
@click.argument('sample-name', type=click.STRING)
def reads_download(sample_name):
    """
    Download reads from cloud storage to local disk.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    reads.download(TenxReads(sample_name=sample_name))
tenx_reads_cmd.add_command(reads_download, name="download")
#-- READS

# REFERENCE
# - download (fetch reference from the cloud)
@click.group()
def tenx_ref_cmd():
    """
    Commands for Reference Sequences
    """
    pass

cli.add_command(tenx_ref_cmd, name="ref")

@click.command(short_help="fetch reference sequences")
@click.argument('ref-name', type=click.STRING)
def ref_download(ref_name):
    """
    Download reference sequences from cloud storage to local disk.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    reference.download(TenxReference(name=ref_name))
tenx_ref_cmd.add_command(ref_download, name="download")

#-- REFERENCE

# UTIL
@click.group()
def tenx_util_cmd():
    """
    Utilities and Helpers
    """
    pass

cli.add_command(tenx_util_cmd, name='util')

@click.command()
@click.argument('directory', type=click.Path(exists=True))
def tenx_util_calculate_compute_metrics(directory):
    """
    Calculate the compute metrics for a 10X genomics pipeline run.
    """
    print( report.compute_metrics_basic(util.calculate_compute_metrics(directory)) )
tenx_util_cmd.add_command(tenx_util_calculate_compute_metrics, name='calculate-compute-metrics')

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
tenx_util_cmd.add_command(tenx_util_verify_upload, name='verify-upload')

#-- UTIL
