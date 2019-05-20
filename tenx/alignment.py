import glob, os, shutil, subprocess, sys, tempfile
from app import TenxApp

class TenxAlignment():

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_URL'], self.sample_name, 'alignment')

    def sample_directory(self):
        return os.path.join(TenxApp.config['TENX_DATA_PATH'], self.sample_name)

    def directory(self):
        return os.path.join(self.sample_directory(), 'alignment')

    def outs_directory(self):
        return os.path.join(self.directory(), 'outs')

    def reads_directory(self):
        return os.path.join(self.sample_directory(), 'reads')

    def is_successful(self):
        return os.path.exists( os.path.join(self.outs_directory(), "summary.csv") )

#-- TenxAlignment
