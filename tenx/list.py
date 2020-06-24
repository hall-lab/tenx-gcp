import click, os, subprocess, tabulate

from tenx.app import TenxApp

def sample_assest_types():
    return ("alignment", "assembly", "reads")

def remote_sample_names():
    remote_url = TenxApp.config['TENX_REMOTE_URL']
    cmd = ["gsutil", "ls", remote_url]
    url_out = subprocess.check_output(cmd)
    sample_names = []
    for sample_url in url_out.decode().splitlines():
        if not sample_url.endswith("/"):
            continue # skip objects that are files
        sample_name = os.path.basename(sample_url.rstrip("/"))
        sample_names.append(sample_name)
    return sample_names

def remote_sample_details(sample_names):
    remote_url = TenxApp.config['TENX_REMOTE_URL']
    samples = {}
    for sample_name in sample_names:
        if sample_name == "loupe_files": continue
        cmd = ["gsutil", "ls", os.path.join(remote_url, sample_name)]
        sample_url_out = subprocess.check_output(cmd)
        items = {}
        sub_urls = list( map(lambda i: os.path.basename(i.rstrip("/")), sample_url_out.decode().splitlines()) )
        for t in sample_assest_types():
            if t in sub_urls:
                items[t] = "Y"
            else:
                items[t] = "N"
        if len(items) > 0:
            samples[sample_name] = items

    return samples

#-- remote
        
@click.command(short_help="list samples and their assests")
@click.argument("sample-names", nargs=-1, type=click.STRING)
def list_cmd(sample_names):
    """
    List REMOTE Samples and Assests [ALN, ASM, RDS]

    Give sample names to see sample assets.  If no sample names given, all samples will be listed. Then use the command again to list specific sample assests.
    """
    if sample_names:
        samples = remote_sample_details(sample_names)
        print_sample_assests(samples)
    else:
        sample_names = remote_sample_names()
        print_sample_names(sample_names)

def print_sample_names(sample_names):
    rows = []
    for sample_name in sample_names:
        rows.append([sample_name])
    print(tabulate.tabulate(rows, ["SAMPLE_NAME"]))

def print_sample_assests(samples):
    rows = []
    for sample_name in samples.keys():
        row = [sample_name, "REMOTE"]
        for t in sample_assest_types():
            row.append(samples[sample_name].get(t))
        rows.append(row)
    print(tabulate.tabulate(rows, ["SAMPLE_NAME", "TYPE", "ALN", "ASM", "RDS"]))

#-- list_cmd
