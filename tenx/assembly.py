import os
from app import TenxApp

class TenxAssembly():

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'assembly')

    def local_directory(self):
        return os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], self.sample_name, 'assembly')

#-- TenxAssembly
