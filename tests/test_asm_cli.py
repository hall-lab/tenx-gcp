import subprocess, unittest

class TenxAsmCliTest(unittest.TestCase):

    # ASSEMBLY
    def test2_tenx_assembly(self):
        rv = subprocess.call(['tenx', 'asm'])
        self.assertEqual(rv, 0)

    def test2_tenx_assembly_assemble(self):
        rv = subprocess.call(['tenx', 'asm', 'assemble', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'asm', 'assemble'])
        self.assertEqual(rv, 2)

    def test2_tenx_assembly_pipeline(self):
        rv = subprocess.call(['tenx', 'asm', 'pipeline', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'asm', 'pipeline'])
        self.assertEqual(rv, 2)

    def test2_tenx_assembly_mkoutput(self):
        rv = subprocess.call(['tenx', 'asm', 'mkoutput', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'asm', 'mkoutput'])
        self.assertEqual(rv, 2)

    def test2_tenx_assembly_upload(self):
        rv = subprocess.call(['tenx', 'asm', 'upload', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'asm', 'upload'])
        self.assertEqual(rv, 2)

# -- TenxAsmCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
