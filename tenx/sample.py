import os

from tenx.assembly import TenxAssembly
from tenx.alignment import TenxAlignment

class TenxSample():
    def __init__(self, base_path, name):
        self.base_path = base_path
        self.name = name
        self.path = os.path.join(self.base_path, name)
        self.reads_path = os.path.join(self.path, 'reads')
        self.pipeline_path = os.path.join(self.path, "pipeline")

    def alignment(self, ref=None):
        return TenxAlignment(sample=self, path=os.path.join(self.path, "alignment"), ref=ref)

    def assembly(self):
        return TenxAssembly(sample=self, path=os.path.join(self.path, "assembly"))

#-- TenxSample
