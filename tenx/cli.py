import click, os, socket, sys, tabulate

from tenx.app import TenxApp
from tenx.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """
    10X CLI
    """
    TenxApp(os.environ.get('TENX_CONFIG_FILE', None))
    pass

# ALIGNMENT
from tenx.aln_cli import tenx_aln_cli
cli.add_command(tenx_aln_cli, name="aln")

# ASSEMBLY
from tenx.asm_cli import tenx_asm_cli
cli.add_command(tenx_asm_cli, name="asm")

# COMPUTE
from tenx.compute_cli import tenx_compute_cli
cli.add_command(tenx_compute_cli, name="compute")

# LIST
from tenx.list import list_cmd
cli.add_command(list_cmd, name="list")

# READS
from tenx.reads_cli import reads_cli
cli.add_command(reads_cli, name="reads")

# REFERENCE
from tenx.ref_cli import tenx_ref_cli
cli.add_command(tenx_ref_cli, name="ref")

# UTIL
from tenx.util_cli import tenx_util_cli
cli.add_command(tenx_util_cli, name="util")
