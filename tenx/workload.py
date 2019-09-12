import jinja2, os, subprocess, sys, tempfile

class Job():

    def __init__(self, name, manager):
        self.name = name
        self.manager = manager

    def from_fn(fn):
        (name, manager, suffix) = f.split(".")
        return Job(name=name, manager=manager)

    #-- __init__    

    def launch_cmd(self):
        if self.manager == 'slurm':
            return "sbatch"
        else:
            raise Exception("Unknown job manager: {}".format(self.name))

    @staticmethod
    def templates_path():
       return os.path.join( os.path.dirname(os.path.abspath(__file__)), "job-templates")

    #-- attrs

    def template_bn(self):
        return ".".join([self.name, self.manager, "sh"])

    def template_fn(self):
        job_templates_p = self.templates_path()
        if not os.path.exists(job_templates_p): raise Exception("Cannot find job templates directory!")
        template_fn = os.path.join(job_templates_p, self.template_bn())
        if not os.path.exists(template_fn): raise Exception("Failed to find job template file: {}".format(template_fn))
        return template_fn

    def load_template(self):
        template_fn = self.template_fn()
        with open(template_fn, 'r') as f:
            job_template = jinja2.Template(f.read())
        return job_template

    #-- job template

    def write_script(self, params, script_fn):
        template = self.load_template()
        with open(script_fn, "w") as f:
            f.write(template.render(params))

    def launch_script(self, params):
        script_f = tempfile.NamedTemporaryFile()
        self.write_script(params=params, script_fn=script_f.name)
        cmd = [self.launch_cmd(), script_f.name]
        sys.stderr.write("RUNNING: {}\n".format(" ".join(cmd)))
        subprocess.check_call(cmd)

    #-- job script

#-- Job
