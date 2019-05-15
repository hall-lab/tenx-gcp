import os, sys, unittest

from .context import tenx
from tenx.app import TenxApp

class TenxAppTest(unittest.TestCase):

    def test1_init_fails(self):
        with self.assertRaises(IOError) as cm:
            TenxApp("/tenx.yaml")
        self.assertTrue("No such file or directory" in cm.exception)

    def test2_init(self):
        # init w/o config
        tenxapp = TenxApp()
        self.assertIsNotNone(TenxApp.config)

        # init w/ config
        TenxApp.config = None
        tenxapp = TenxApp("tests/test_app/tenx.yaml")
        self.assertIsNotNone(tenxapp)
        self.assertIsNotNone(tenxapp.config)
        self.assertEqual(tenxapp.config['environment'], 'test')

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
