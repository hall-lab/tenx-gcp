import click, os

from tenx.version import __version__
from tenx import app, reads, report, util

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """
    10X CLI
    """
    app.TenxApp(os.environ.get('TENX_CONFIG', None))
    pass

# ASSEMBLY
# - asm (run supernova only command)
# - mkoutput (runs mkputput on an assembly
# - pipeline (run-supernova - full pipeline)
# - upload (sends assembly to object store)
# FUTURE download, list, view

@click.group()
def assembly():
    """
    Commands, Pipeline, and Helpers for Assemblies
    """
    pass

cli.add_command(assembly)

@click.command(short_help="create an assembly with supernova")
@click.argument('sample-name', type=click.STRING)
def asm_assemble(sample_name):
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_assemble(assembly.TenxAssembly(sample_name=sample_name))
assembly.add_command(asm_assemble, name="assemble")

@click.command(short_help="run mkoutput on an assembly")
@click.argument('sample-name', type=click.STRING)
def asm_mkoutput(sample_name):
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_mkoutput(assembly.TenxAssembly(sample_name=sample_name))
assembly.add_command(asm_mkoutput, name="mkoutput")

@click.command(short_help="run the full supernova assembly pipeline")
@click.argument('sample-name', type=click.STRING)
def asm_pipeline(sample_name):
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    reads.download(reads.TenxReads(sample_name=sample_name))
    asm = assembly.TenxAssembly(sample_name=sample_name)
    assembly.run_assemble(asm)
    assembly.run_mkoutput(asm)
    print( report.run_duration_basic(util.run_duration(asm.directory)) )
    assembly.run_upload(asm)
assembly.add_command(asm_pipeline, name="pipeline")

@click.command(short_help="Send the assembly to the cloud")
@click.argument('sample-name', type=click.STRING)
def asm_upload(sample_name):
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_mkoutput(assembly.TenxAssembly(sample_name=sample_name))
assembly.add_command(asm_upload, name="upload")
#-- ASSEMBLY

# READS
# - download (fetch reads from the cloud)
@click.group(name="reads")
def reads_cli():
    """
    Commands and Helpers for 10X Reads
    """
    pass

cli.add_command(reads_cli)

@click.command(short_help="Download reads from the cloud!")
@click.argument('sample-name', type=click.STRING)
def reads_download(sample_name):
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    reads.download(reads.TenxReads(sample_name=sample_name))
reads_cli.add_command(reads_download, name="download")
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
def tenx_util_runduration(directory):
    print( report.run_duration_basic(util.run_duration(directory)) )
tenx_util_cmd.add_command(tenx_util_runduration, name='run-duration')
#-- UTIL
