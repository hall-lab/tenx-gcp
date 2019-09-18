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
from compute_cli import tenx_compute_cli
cli.add_command(tenx_compute_cli, name="compute")

# READS
from reads_cli import tenx_reads_cli
cli.add_command(tenx_reads_cli, name="reads")

# REFERENCE
from ref_cli import tenx_ref_cli
cli.add_command(tenx_ref_cli, name="ref")

# UTIL
from util_cli import tenx_util_cli
cli.add_command(tenx_util_cli, name="util")
