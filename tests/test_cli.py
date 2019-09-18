import subprocess, unittest

class TenxCliTest(unittest.TestCase):

    def test1_tenx(self):
        rv = subprocess.call(['tenx'])
        self.assertEqual(rv, 0)

    def test4_tenx_util(self):
        rv = subprocess.call(['tenx', 'util'])
        self.assertEqual(rv, 0)

    def test4_tenx_reads_download(self):
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics'])
        self.assertEqual(rv, 2)

# -- TenxCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
