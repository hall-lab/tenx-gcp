import click, os

from tenx.version import __version__
from tenx import app, reads

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
# - run (run-supernova - full pipeline)
# - upload (sends assembly to object store)
# FUTURE download, list, view

@click.group()
def assembly():
    """
    Commands, Pipeline, and Helpers for Assemblies
    """
    pass

cli.add_command(assembly)

@click.command()
def asm():
    click.echo("ASM")
assembly.add_command(asm)

@click.command()
def mkoutput():
    click.echo("MKOUTPUT")
assembly.add_command(mkoutput)

@click.command()
def run():
    click.echo("RUN")
assembly.add_command(run)

@click.command()
def upload():
    click.echo("UPLOAD")
assembly.add_command(upload)
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