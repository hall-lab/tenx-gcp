import click, os, socket, sys

import tenx.app as app
from tenx.version import __version__
from tenx import app, alignment, assembly, reads, reference, report, util
from alignment import TenxAlignment
from reads import TenxReads
from reference import TenxReference
import notifications

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
# - align
# - pipeline (dl rds, dl ref, aln, ul aln)
# - upload
@click.group()
def tenx_aln_cmd():
    """
    Commands, Pipeline, and Helpers for Alignments
    """
    pass

cli.add_command(tenx_aln_cmd, name="alignment")

@click.command(short_help="align with longranger")
@click.argument('sample-name', type=click.STRING)
@click.argument('ref-name', type=click.STRING)
def aln_align(sample_name, ref_name):
    """
    Create alignments with longranger.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    alignment.run_align(TenxAlignment(sample_name=sample_name), TenxReads(sample_name=sample_name), TenxReference(name=ref_name))
tenx_aln_cmd.add_command(aln_align, name="align")

@click.command(short_help="align with longranger")
@click.argument('sample-name', type=click.STRING)
@click.argument('ref-name', type=click.STRING)
def aln_pipeline(sample_name, ref_name):
    """
    Fully automated pipeline to create longranger alignments.

    Process includes: downloading reads & reference, running longranger, and then uploading the alignments to the cloud.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
tenx_aln_cmd.add_command(aln_pipeline, name="pipeline")

@click.command(short_help="to the cloud")
@click.argument('sample-name', type=click.STRING)
def aln_upload(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    alignment.run_upload(alignment.TenxAlignment(sample_name=sample_name))
tenx_aln_cmd.add_command(aln_upload, name="upload")

# ASSEMBLY
# - asm (run supernova only command)
# - mkoutput (runs mkputput on an assembly
# - pipeline (run-supernova - full pipeline)
# - upload (sends assembly to object store)

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
    """
    Create an assembly with supernova.
    """
    assert bool(app.TenxApp.config) is True, "Must provide tenx yaml config file!"
    assembly.run_assemble(assembly.TenxAssembly(sample_name=sample_name))
tenx_assembly_cmd.add_command(asm_assemble, name="assemble")

@click.command(short_help="run mkoutput on an assembly")
@click.argument('sample-name', type=click.STRING)
def asm_mkoutput(sample_name):
    """
    Run mkoutput on a supernova assembly.
    """
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
tenx_assembly_cmd.add_command(asm_pipeline, name="pipeline")

@click.command(short_help="Send the assembly to the cloud")
@click.argument('sample-name', type=click.STRING)
def asm_upload(sample_name):
    """
    Upload an assembly from local disk to cloud storage.
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
