import os, unittest

from tenx.app import TenxApp
from tenx.sample import TenxSample

class TenxSampleTest(unittest.TestCase):

    def setUp(self):
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = "/mnt/disks/data"
        TenxApp.config['TENX_REMOTE_URL'] = "gs://data"

    def tearDown(self):
        TenxApp.config = None

    def test0_sample(self):
        for key in "TENX_DATA_PATH", "TENX_REMOTE_URL":
            base_path = TenxApp.config.get(key)
            s = TenxSample(base_path=base_path, name="TEST-001")
            self.assertEqual(s.base_path, base_path)
            self.assertEqual(s.name, "TEST-001")
            self.assertEqual(s.path, os.path.join(base_path, "TEST-001"))
            self.assertEqual(s.reads_path, os.path.join(base_path, "TEST-001", "reads"))

# -- TenxSampleTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
