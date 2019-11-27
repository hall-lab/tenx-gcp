import click, os, sys, tabulate

from tenx.compute import Job

# COMPUTE
# - list-templates
# - submit
@click.group(name="compute")
def tenx_compute_cli():
    """
    Commands to work with resources to submit jobs to a compute manager.
    """
    pass

@click.command(short_help="List available job templates")
def compute_list_templates():
    """
    List compute job templates and details.
    """
    rows = []
    for fn in os.listdir( Job.templates_path() ):
        print("\n\n"+fn+"\n\n")
        (name, manager, suffix) = fn.split(".")
        info = Job.load_template_yaml(fn)
        rows += [[ name, manager, " ".join(info["PARAMS"].keys()) ]]
    sys.stdout.write( tabulate.tabulate(rows, ["NAME", "MANAGER", "PARAMS"], tablefmt="simple") )
tenx_compute_cli.add_command(compute_list_templates, name="list-templates")

@click.command(short_help="Submit a job to a compute cluster")
@click.argument('template', type=click.STRING)
@click.argument('manager', type=click.STRING)
@click.option('--params', type=click.STRING, required=True, help="Parameters for the job template as comma separated key=value pairs. Ex: SAMPLE_NAME=mysample,REF_NAME=grc38")
def compute_submit(template, manager, params):
    """
    Submit a job template to a compute manager with specified parameters.

    See `list-template` sub-command for availble job templates and their params.
    """
    job = Job(name=template, manager=manager)
    sys.stderr.write("Template: {}\nManager: {}\n".format(template, manager))
    job.launch_script(params)
tenx_compute_cli.add_command(compute_submit, name="submit")

# -- COMPUTE
