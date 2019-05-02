import click

from tenx.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """
    10X CLI
    """

# ASSEMBLY
# - asm (run supernova only command)
# - mkoutput (runs mkputput on an assembly
# - run (run-supernova - full pipeline)
# - upload (sends assembly to object store)
# FUTURE download, list, view

@click.group()
def assembly():
    """
    Commands, Pipeline, and Helpers for Supernova Assemblies 
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
