import click, glob, os, subprocess, sys
from tenx.app import TenxApp
from tenx.sample import TenxSample

@click.command()
@click.argument("sample_name")
def ul_cmd(sample_name):
    """
    Upload reads to remote storage
    """
    lsample = TenxSample(base_path=TenxApp.config.get("TENX_DATA_PATH"), name=sample_name)
    rsample = TenxSample(base_path=TenxApp.config.get("TENX_REMOTE_URL"), name=sample_name)
    ul(lsample, rsample)

def ul(lsample, rsample):
    sys.stderr.write("Upload {0} reads fastqs to the object store via sync...\n".format(lsample.name))

    ldir = lsample.reads_path
    sys.stderr.write("Checking for fastqs in {0}\n".format(ldir))
    if not os.path.exists(ldir):
        raise Exception("Sample reads path does not exist!")
    os.chdir(ldir)
    fastqs = glob.glob('*fastq*')
    if len(fastqs) == 0:
        raise Exception("Did find any fastqs in reads path!")
    sys.stderr.write("Found {} fastq(s)\n".format(len(fastqs)))

    sys.stderr.write("Upload to {}\n".format(rsample.reads_path))
    subprocess.check_call(["gsutil", "-m", "rsync", "-r", ".", rsample.reads_path])
    fastqs = glob.glob("*fastq*")
    if len(fastqs) == 0:
        raise Exception("Failed to download read fastqs!")

    sys.stderr.write("Done\n")

#-- download
