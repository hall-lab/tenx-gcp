import subprocess, unittest

class TenxRefCliTest(unittest.TestCase):

    def test1_tenx_ref(self):
        rv = subprocess.call(['tenx', 'ref'])
        self.assertEqual(rv, 0)

    def test2_tenx_ref_download(self):
        rv = subprocess.call(['tenx', 'ref', 'download', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'ref', 'download'])
        self.assertEqual(rv, 2)

# -- TenxRefCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
