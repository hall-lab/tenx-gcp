import subprocess, unittest

class TenxCliTest(unittest.TestCase):

    def test2_tenx_compute(self):
        rv = subprocess.call(['tenx', 'compute'])
        self.assertEqual(rv, 0)

    def test2_tenx_compute_list_templates(self):
        rv = subprocess.call(['tenx', 'compute', 'list-templates', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'compute', 'list-templates'])
        self.assertEqual(rv, 0)

    def test2_tenx_compute_submit(self):
        rv = subprocess.call(['tenx', 'compute', 'submit', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'compute', 'submit'])
        self.assertEqual(rv, 2)

# -- TenxCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
