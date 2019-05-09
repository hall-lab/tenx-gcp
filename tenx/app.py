import logging, yaml

class TenxApp(object):
    def __init__(self, config_fn=None):
        '''
        Tenx App with YAML Config
        '''
        self.config = None
        if config_fn is not None:
            logging.getLogger('root').info('Using config at {0}'.format(config_fn))
            with open(config_fn, 'r') as f:
                self.config = yaml.safe_load(f)

    # -- __init

# -- TenxApp
