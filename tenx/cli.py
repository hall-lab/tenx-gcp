import click, os, sys

from tenx.version import __version__
from tenx import app, assembly, reads, report, util

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """
    10X CLI
    """
    app.TenxApp(os.environ.get('TENX_CONFIG_FILE', None))
    pass

# ASSEMBLY
# - asm (run supernova only command)
# - mkoutput (runs mkputput on an assembly
# - pipeline (run-supernova - full pipeline)
# - upload (sends assembly to object store)
# FUTURE download, list, view

@click.group()
def tenx_assembly_cmd():
    """
    Commands, Pipeline, and Helpers for Assemblies
    """
    pass

cli.add_command(tenx_assembly_cmd, name="assembly")

@click.command(short_help="create an assembly with supernova")
@click.argument('sample-name', type=click.STRING)
def asm_assemble(sample_name):
    """Create an assembly with supernova."""
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_assemble(assembly.TenxAssembly(sample_name=sample_name))
tenx_assembly_cmd.add_command(asm_assemble, name="assemble")

@click.command(short_help="run mkoutput on an assembly")
@click.argument('sample-name', type=click.STRING)
def asm_mkoutput(sample_name):
    """Run mkoutput on a supernova assembly."""
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_mkoutput(assembly.TenxAssembly(sample_name=sample_name))
tenx_assembly_cmd.add_command(asm_mkoutput, name="mkoutput")

@click.command(short_help="run the full supernova assembly pipeline")
@click.argument('sample-name', type=click.STRING)
def asm_pipeline(sample_name):
    """
    Fully automated pipeline to create a supernova assembly.

    Process includes: downloading reads, running supernova, mkoutput, and then uploading the assembly.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    sys.stderr.write("Run assembly pipeline for {}".format(sample_name))
    reads.download(reads.TenxReads(sample_name=sample_name))
    asm = assembly.TenxAssembly(sample_name=sample_name)
    assembly.run_assemble(asm)
    assembly.run_mkoutput(asm)
    compute_metrics = util.calculate_compute_metrics(asm.directory())
    print( report.compute_metrics_basic(compute_metrics) )
    with open(os.path.join(asm.directory(), "outs", "compute-metrics.txt"), "w") as f:
        f.write( report.compute_metrics_basic(metrics=compute_metrics) )
    assembly.run_upload(asm)
    sys.stderr.write("Run assembly pipeline...OK")
tenx_assembly_cmd.add_command(asm_pipeline, name="pipeline")

@click.command(short_help="Send the assembly to the cloud")
@click.argument('sample-name', type=click.STRING)
def asm_upload(sample_name):
    """
    Upload an assembly from the local directory to cloud storage.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_upload(assembly.TenxAssembly(sample_name=sample_name))
tenx_assembly_cmd.add_command(asm_upload, name="upload")
#-- ASSEMBLY

# READS
# - download (fetch reads from the cloud)
@click.group(name="reads")
def tenx_reads_cmd():
    """
    Commands and Helpers for 10X Reads
    """
    pass

cli.add_command(tenx_reads_cmd)

@click.command(short_help="Download reads from the cloud!")
@click.argument('sample-name', type=click.STRING)
def reads_download(sample_name):
    """
    Download reads from cloud storage to local directory.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    reads.download(reads.TenxReads(sample_name=sample_name))
tenx_reads_cmd.add_command(reads_download, name="download")
#-- READS

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
def tenx_util_verify_upload(directory, remote_url):
    """
    Check if all files from LOCAL directory are on REMOTE url.
    """
    sys.stderr.write("Local directory: {}\n".format(directory))
    sys.stderr.write("Remote URL: {}\n".format(remote_url))
    util.verify_upload(ldir=directory, rurl=remote_url)
    sys.stderr.write("All local files found on remote!")
tenx_util_cmd.add_command(tenx_util_verify_upload, name='verify-upload')
#-- UTIL
