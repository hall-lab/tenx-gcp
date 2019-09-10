import jinja2, os

class Job():

    def __init__(self, name, manager):
        self.name = name
        self.manager = manager

    #-- __init__    

    def launch_cmd(self):
        if self.manager == 'slurm':
            return "sbatch"
        else:
            raise Exception("Unknown job manager: {}".format(self.name))

    def template_fn(self):
        job_templates_p = os.path.join( os.path.dirname(os.path.abspath(__file__)), "job-templates")
        if not os.path.exists(job_templates_p): raise Exception("Cannot find job templates directory!")
        template_fn = os.path.join(job_templates_p, ".".join([self.name, self.launch_cmd(), "sh"]))
        if not os.path.exists(template_fn): raise Exception("Failed to find job template file: {}".format(template_fn))
        return template_fn

    def load_template(self):
        template_fn = self.template_fn()
        with open(template_fn, 'r') as f:
            job_template = jinja2.Template(f.read())
        return job_template

    #-- job template

#-- Job
