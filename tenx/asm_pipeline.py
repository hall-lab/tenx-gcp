import click, os, socket, sys

from tenx.app import TenxApp
import tenx.assembly as assembly
import tenx.notifications as notifications
import tenx.reads as reads
import tenx.report as report
import tenx.util as util

@click.command(short_help="run the full supernova assembly pipeline")
@click.argument('sample-name', type=click.STRING)
def asm_pipeline_cmd(sample_name):
    """
    Fully automated pipeline to create a supernova assembly.

    Process includes: downloading reads, running supernova, mkoutput, and then uploading the assembly.
    """
    assert bool(TenxApp.config) is True, "Must provide tenx yaml config file!"
    sys.stderr.write("Run assembly pipeline for {}".format(sample_name))
    notifications.slack("{} START {}".format(sample_name, socket.gethostname()))
    try:
        reads.download(reads.TenxReads(sample_name=sample_name))
        asm = assembly.TenxAssembly(sample_name=sample_name)
        assembly.run_assemble(asm)
        assembly.run_mkoutput(asm)
        compute_metrics = util.calculate_compute_metrics(asm.directory())
        print( report.compute_metrics_basic(compute_metrics) )
        with open(os.path.join(asm.directory(), "outs", "compute-metrics.txt"), "w") as f:
            f.write( report.compute_metrics_basic(metrics=compute_metrics) )
        run_upload(asm, assembly.TenxAssembly(sample_name=sample_name, base_path=TenxApp.config["TENX_REMOTE_URL"]))
        sys.stderr.write("Run assembly pipeline...OK")
    except BaseException as ex:
        sys.stderr.write("Exception: {}\n".format(ex))
        sys.stderr.write("Exception encountered, sending notifications if configured...\n")
        notifications.slack("{} FAILED {}".format(sample_name, socket.gethostname()))
        raise
    sys.stderr.write("Finished, sending notifications if configured...\n")
    notifications.slack("{} SUCCESS {}".format(sample_name, socket.gethostname()))
