import os, subprocess, sys, unittest

from .context import tenx

class TenxCliTest(unittest.TestCase):

    def test1_tenx(self):
        rv = subprocess.call(['tenx'])
        self.assertEqual(rv, 0)

    def test2_tenx_assembly(self):
        rv = subprocess.call(['tenx', 'assembly'])
        self.assertEqual(rv, 0)

    def test3_tenx_reads(self):
        rv = subprocess.call(['tenx', 'reads'])
        self.assertEqual(rv, 0)

    def test3_tenx_reads_download(self):
        rv = subprocess.call(['tenx', 'reads', 'download', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'reads', 'download'])
        self.assertEqual(rv, 2)

# -- TenxCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
