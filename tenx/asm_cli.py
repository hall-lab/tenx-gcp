import click, os, socket, sys

import tenx.app as app
from tenx import app, assembly, reads, report, util
from .assembly import TenxAssembly
from .reads import TenxReads
import notifications
from compute import Job

# ASSEMBLY
# - assemble (run supernova only command)
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
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_assemble(assembly.TenxAssembly(sample_name=sample_name))
tenx_asm_cli.add_command(asm_assemble, name="assemble")

@click.command(short_help="run mkoutput on an assembly")
@click.argument('sample-name', type=click.STRING)
def asm_mkoutput(sample_name):
    """
    Run mkoutput on a supernova assembly.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_mkoutput(assembly.TenxAssembly(sample_name=sample_name))
tenx_asm_cli.add_command(asm_mkoutput, name="mkoutput")

@click.command(short_help="run the full supernova assembly pipeline")
@click.argument('sample-name', type=click.STRING)
def asm_pipeline(sample_name):
    """
    Fully automated pipeline to create a supernova assembly.

    Process includes: downloading reads, running supernova, mkoutput, and then uploading the assembly.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    sys.stderr.write("Run assembly pipeline for {}".format(sample_name))
    notifications.slack("{} START {}".format(sample_name, socket.gethostname()))
    try:
        reads.download(TenxReads(sample_name=sample_name))
        asm = assembly.TenxAssembly(sample_name=sample_name)
        assembly.run_assemble(asm)
        assembly.run_mkoutput(asm)
        compute_metrics = util.calculate_compute_metrics(asm.directory())
        print( report.compute_metrics_basic(compute_metrics) )
        with open(os.path.join(asm.directory(), "outs", "compute-metrics.txt"), "w") as f:
            f.write( report.compute_metrics_basic(metrics=compute_metrics) )
        assembly.run_upload(asm)
        sys.stderr.write("Run assembly pipeline...OK")
    except BaseException as ex:
        sys.stderr.write("Exception: {}\n".format(ex))
        sys.stderr.write("Exception encountered, sending notifications if configured...\n")
        notifications.slack("{} FAILED {}".format(sample_name, socket.gethostname()))
        raise
    sys.stderr.write("Finished, sending notifications if configured...\n")
    notifications.slack("{} SUCCESS {}".format(sample_name, socket.gethostname()))
tenx_asm_cli.add_command(asm_pipeline, name="pipeline")

@click.command(short_help="Send the assembly to the cloud")
@click.argument('sample-name', type=click.STRING)
def asm_upload(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_upload(assembly.TenxAssembly(sample_name=sample_name))
tenx_asm_cli.add_command(asm_upload, name="upload")

#-- ASSEMBLY
