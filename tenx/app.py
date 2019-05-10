import logging, yaml

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

# -- TenxApp
