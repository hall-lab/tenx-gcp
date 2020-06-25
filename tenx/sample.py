import os

from tenx.assembly import TenxAssembly

class TenxSample():
    
    def __init__(self, base_path, name):
        self.base_path = base_path
        self.name = name
        self.path = os.path.join(self.base_path, name)
        self.reads_path = os.path.join(self.path, 'reads')

    def assembly(self):
        return TenxAssembly(sample=self, path=os.path.join(self.path, "assembly"))

#-- TenxSample
