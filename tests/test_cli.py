import os, subprocess, sys, unittest

from .context import tenx

class TenxCliTest(unittest.TestCase):

    def test1_tenx(self):
        rv = subprocess.call(['tenx'])
        self.assertEqual(rv, 0)

    # ALIGNMENT
    def test2_tenx_alignment(self):
        rv = subprocess.call(['tenx', 'alignment'])
        self.assertEqual(rv, 0)

    def test2_tenx_alignment_align(self):
        rv = subprocess.call(['tenx', 'alignment', 'align', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'alignment', 'align'])
        self.assertEqual(rv, 2)

    def test2_tenx_alignment_pipeline(self):
        rv = subprocess.call(['tenx', 'alignment', 'pipeline', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'alignment', 'pipeline'])
        self.assertEqual(rv, 2)

    def test2_tenx_alignment_upload(self):
        rv = subprocess.call(['tenx', 'alignment', 'upload', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'alignment', 'upload'])
        self.assertEqual(rv, 2)

    # ASSEMBLY
    def test2_tenx_assembly(self):
        rv = subprocess.call(['tenx', 'assembly'])
        self.assertEqual(rv, 0)

    def test2_tenx_assembly_assemble(self):
        rv = subprocess.call(['tenx', 'assembly', 'assemble', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'assembly', 'assemble'])
        self.assertEqual(rv, 2)

    def test2_tenx_assembly_pipeline(self):
        rv = subprocess.call(['tenx', 'assembly', 'pipeline', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'assembly', 'pipeline'])
        self.assertEqual(rv, 2)

    def test2_tenx_assembly_mkoutput(self):
        rv = subprocess.call(['tenx', 'assembly', 'mkoutput', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'assembly', 'mkoutput'])
        self.assertEqual(rv, 2)

    def test2_tenx_assembly_upload(self):
        rv = subprocess.call(['tenx', 'assembly', 'upload', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'assembly', 'upload'])
        self.assertEqual(rv, 2)

    # READS
    def test3_tenx_reads(self):
        rv = subprocess.call(['tenx', 'reads'])
        self.assertEqual(rv, 0)

    def test3_tenx_reads_download(self):
        rv = subprocess.call(['tenx', 'reads', 'download', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'reads', 'download'])
        self.assertEqual(rv, 2)

    def test4_tenx_util(self):
        rv = subprocess.call(['tenx', 'util'])
        self.assertEqual(rv, 0)

    def test4_tenx_reads_download(self):
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics'])
        self.assertEqual(rv, 2)

    # REFERENCE
    def test2_tenx_ref(self):
        rv = subprocess.call(['tenx', 'ref'])
        self.assertEqual(rv, 0)

    def test2_tenx_ref_download(self):
        rv = subprocess.call(['tenx', 'ref', 'download', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'ref', 'download'])
        self.assertEqual(rv, 2)

# -- TenxCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
