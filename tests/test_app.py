import os, sys, unittest

from .context import tenx
import tenx.app as app

class TenxAppTest(unittest.TestCase):

    def test_init(self):
        # init w/ config
        theapp = app.TenxApp("tests/test_app/tenx.yaml")
        self.assertIsNotNone(theapp)
        self.assertIsNotNone(theapp.config)
        self.assertEqual(theapp.config['environment'], 'test')

        # init w/o config
        theapp = app.TenxApp()
        self.assertIsNone(theapp.config)

    def test_init_fails(self):
        with self.assertRaises(IOError) as cm:
            app.TenxApp("/tenx.yaml")
        self.assertTrue("No such file or directory" in cm.exception)

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
