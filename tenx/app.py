import jinja2, json, logging, os, yaml

class TenxApp(object):
    config = None # class variable, used as a singleton for the app config
    def __init__(self, config_fn=None):
        '''
        Tenx App with YAML Config
        '''
        if TenxApp.config is not None: raise Exception("Trying to re-initialize the TenxApp!")
        if config_fn is not None:
            logging.getLogger('root').info('Initializing TenxApp with config file: {0}'.format(config_fn))
            with open(config_fn, 'r') as f:
                TenxApp.config = yaml.safe_load(f)
        else:
            logging.getLogger('root').info('Initializing TenxApp without a config file')
            TenxApp.config = {}

    # -- __init

    @staticmethod
    def load_script_template(name):
        if not 'TENX_SCRIPTS_PATH' in TenxApp.config.keys(): raise Exception("Scripts directory (TENX_SCRIPTS_PATH) is not set in tenx config!")
        script_fn = os.path.join(TenxApp.config['TENX_SCRIPTS_PATH'], name + '.jinja')
        if not os.path.exists(script_fn): raise Exception("Failed to find script template file: {}".format(script_fn))
        with open(script_fn, 'r') as f:
            script_template = jinja2.Template(f.read())
        return script_template

#-- load_script_template

# -- TenxApp

class TenxCromwell():
    def __init__(self):
        if not TenxApp.config:
            raise Exception("Tenx config has not been initialized!")

        self.cromwell_dn = TenxApp.config.get("TENX_CROMWELL_PATH", None)
        if not self.cromwell_dn:
            raise Exception("Cromwell path not found in Tenx config!")
        if not os.path.exists(self.cromwell_dn):
            raise Exception("Cromwell path set in tenx config at {} does not exist!".format(self.cromwell_dn))

        self.cromwell_jar = os.path.join(self.cromwell_dn, "cromwell.jar")
        if not os.path.exists(self.cromwell_jar):
            raise Exception("Cromwell jar not found at {}!".format(self.cromwell_jar))

    def templates_dn(self):
        return os.path.join(os.path.dirname(__file__), "templates", "cromwell")

    def inputs_bn(self):
        return ".".join(["supernova", "inputs", "json"])

    def wdl_bn(self):
        return ".".join(["supernova", "gcloud", "wdl"])

    def conf_bn(self):
        return ".".join(["supernova", "conf"])

    def supernova_command(self, asm):
        templates_dn = self.templates_dn()
        pipeline_dn = asm.pipeline_path
        if not os.path.exists(pipeline_dn):
            os.makedirs(pipeline_dn)

        # Write Inputs
        inputs_bn = self.inputs_bn()
        inputs_template_fn = os.path.join(templates_dn, inputs_bn)
        with open(inputs_template_fn, "r") as f:
            inputs_str = f.read()
        inputs_t = jinja2.Template(inputs_str)
        inputs_rendered = inputs_t.render(SAMPLE_NAME=asm.sample_name)
        inputs = json.loads(inputs_rendered)
        inputs_fn = os.path.join(pipeline_dn, inputs_bn)
        with open(inputs_fn, "w") as f:
            f.write(json.dumps(inputs))

        # Write WDL
        wdl_bn = self.wdl_bn()
        wdl_template_fn = os.path.join(templates_dn, wdl_bn)
        wdl_fn = os.path.join(pipeline_dn, wdl_bn)
        with open(wdl_template_fn, "r") as in_f, open(wdl_fn, "w") as out_f:
            out_f.write(in_f.read())

        # Write CONF
        conf_bn = self.conf_bn()
        conf_template_fn = os.path.join(templates_dn, conf_bn)
        with open(conf_template_fn, "r") as f:
            conf_str = f.read()
        conf_t = jinja2.Template(conf_str)
        conf_rendered = conf_t.render(CROMWELL_ROOT=pipeline_dn)
        conf_fn = os.path.join(pipeline_dn, conf_bn)
        with open(conf_fn, "w") as f:
            f.write(conf_rendered)

        return ["java", "-Dconfig.file={}".format(conf_fn), "-jar", self.cromwell_jar, "run", wdl_fn, "-i", inputs_fn]

#-- TenxCromwell
