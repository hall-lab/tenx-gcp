import os, sys, unittest
from mock import patch

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

        # re-init w/ config
        TenxApp.config = None
        self.assertIsNone(TenxApp.config)
        tenxapp = TenxApp( os.path.join("tests", "test_app", "tenx.yaml") )
        self.assertIsNotNone(tenxapp)
        self.assertIsNotNone(tenxapp.config)
        self.assertEqual(tenxapp.config['environment'], 'test')

    def test3_script_template(self):
        scripts_path = TenxApp.config.pop('TENX_SCRIPTS_PATH')
        with self.assertRaisesRegexp(Exception, "Scripts directory \(TENX_SCRIPTS_PATH\) is not set in tenx config\!"):
            TenxApp.load_script_template('blah')

        TenxApp.config['TENX_SCRIPTS_PATH'] = scripts_path
        with self.assertRaisesRegexp(Exception, "Failed to find script template file: {}". format(os.path.join(TenxApp.config['TENX_SCRIPTS_PATH'], 'blah.jinja'))):
            TenxApp.load_script_template('blah')

        script_template = TenxApp.load_script_template('foo')
        self.assertIsNotNone(script_template)

    @patch('os.path.dirname')
    def test4_job_template(self, dirname_patch):
        dirname_patch.return_value = os.path.join("/")
        with self.assertRaisesRegexp(Exception, "Cannot find job templates directory!"):
            TenxApp.load_job_template('aln-pipeline.sbatch.sh')

        dirname_patch.return_value = os.path.join("tenx")
        script_template = TenxApp.load_job_template('aln-pipeline.sbatch')
        self.assertIsNotNone(script_template)

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
