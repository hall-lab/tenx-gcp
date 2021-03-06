import click

from tenx.app import TenxApp
import tenx.assembly
from tenx.sample import TenxSample

# ASSEMBLY
# - assemble (run supernova only command)
# - download (run supernova only command)
# - mkoutput (runs mkputput on an assembly
# - pipeline (run-supernova - full pipeline)
# - upload (sends assembly to object store)

@click.group()
def tenx_asm_cli():
    """
    Commands, Pipeline, and Helpers for Assemblies
    """
    pass

@click.command(short_help="create an assembly with supernova")
@click.argument('sample-name', type=click.STRING)
def asm_assemble(sample_name):
    """
    Create an assembly with supernova.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    tenx.assembly.run_assemble(TenxSample(name=sample_name, base_path=TenxApp.config["TENX_DATA_PATH"]).assembly())
tenx_asm_cli.add_command(asm_assemble, name="assemble")

# [download]
from tenx.asm_download import asm_download_cmd
tenx_asm_cli.add_command(asm_download_cmd, name="download")

@click.command(short_help="run mkoutput on an assembly")
@click.argument('sample-name', type=click.STRING)
def asm_mkoutput(sample_name):
    """
    Run mkoutput on a supernova assembly.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    tenx.assembly.run_mkoutput(TenxSample(name=sample_name, base_path=TenxApp.config["TENX_DATA_PATH"]).assembly())
tenx_asm_cli.add_command(asm_mkoutput, name="mkoutput")

# [pipeline]
from tenx.asm_pipeline import asm_pipeline_cmd
tenx_asm_cli.add_command(asm_pipeline_cmd, name="pipeline")

@click.command(short_help="remove unnecessary post assembly files")
@click.argument('sample-name', type=click.STRING)
def asm_cleanup_cmd(sample_name):
    """
    Cleanup Assembly

    This command removes unneeded post assembly file including the "outs/assembly" and "ASSEMBLER_CS" directories.

    It first ensures the 4 mkoutput files are generated.

    Additionally, the "outs/assembly/stats" directory is relocated to "outs".

    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    tenx.assembly.run_cleanup(TenxSample(name=sample_name, base_path=TenxApp.config.get("TENX_REMOTE_URL")).assembly())
tenx_asm_cli.add_command(asm_cleanup_cmd, name="cleanup")

# stats
from tenx.asm_stats import asm_stats_cmd
tenx_asm_cli.add_command(asm_stats_cmd, name="stats")

# upload
from tenx.asm_upload import asm_upload_cmd
tenx_asm_cli.add_command(asm_upload_cmd, name="upload")
