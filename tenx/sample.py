import os


class TenxSample():
    
    def __init__(self, base_path, name):
        self.base_path = base_path
        self.name = name
        self.path = os.path.join(self.base_path, name)
        self.reads_path = os.path.join(self.path, 'reads')

#-- TenxSample
