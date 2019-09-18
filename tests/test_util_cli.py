import subprocess, unittest

class TenxUtilCliTest(unittest.TestCase):

    def test1_tenx_util(self):
        rv = subprocess.call(['tenx', 'util'])
        self.assertEqual(rv, 0)

    def test2_tenx_util_calc_compute_metrics(self):
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics'])
        self.assertEqual(rv, 2)

    def test2_tenx_util_verify_upload(self):
        rv = subprocess.call(['tenx', 'util', 'verify-upload', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'util', 'verify-upload'])
        self.assertEqual(rv, 2)

# -- TenxUtilCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
