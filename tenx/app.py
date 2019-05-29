import jinja2, logging, os, yaml

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

#-- load_script_template_for

# -- TenxApp
