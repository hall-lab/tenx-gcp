import os, sys, tempfile, unittest, yaml
from mock import patch

from .context import tenx
from tenx.app import TenxApp

class TenxAppTest1(unittest.TestCase):

    def setUp(self):
        if TenxApp.config is not None: TenxApp.config = None

    def tearDown(self):
        TenxApp.config = None

    def test1_init_fails(self):
        if TenxApp.config is None: TenxApp()
        TenxApp.config = None
        with self.assertRaisesRegex(IOError, "No such file or directory"):
            TenxApp("/tenx.yaml")

    def test2_init(self):
        # init w/o config
        tenxapp = TenxApp()
        self.assertIsNotNone(TenxApp.config)

        # re-init w/ config
        TenxApp.config = None
        self.assertIsNone(TenxApp.config)

        conf_f = tempfile.NamedTemporaryFile()
        config = {
                "environment": "test",
                "TENX_SCRIPTS_PATH": "tests/test_app",
                "TENX_NOTIFICATIONS_SLACK": "https://slack.com",
                }
        conf_f.write( yaml.dump(config).encode() )
        conf_f.flush()

        tenxapp = TenxApp(conf_f.name)
        self.assertIsNotNone(tenxapp)
        self.assertDictEqual(tenxapp.config, config)

    def test3_templates(self):
        app = TenxApp()
        with self.assertRaisesRegex(BaseException, "Failed to find templates directory for blah"):
            app.templates_dn_for("blah")
        app.templates_dn_for("cromwell")

#-- TenxAppTest1

class TenxAppTest2(unittest.TestCase):

    def setUp(self):
        TenxApp()
        self.scripts_path = tempfile.TemporaryDirectory()
        with open(os.path.join(self.scripts_path.name, "foo.jinja"), "w") as f:
            f.write("FOO JINJA TEMPLATE")

    def tearDown(self):
        self.scripts_path.cleanup()
        TenxApp.config = None

    def test1_script_template(self):
        with self.assertRaisesRegex(Exception, "Scripts directory \(TENX_SCRIPTS_PATH\) is not set in tenx config\!"):
            TenxApp.load_script_template('blah')

        TenxApp.config['TENX_SCRIPTS_PATH'] = self.scripts_path.name
        with self.assertRaisesRegex(Exception, "Failed to find script template file: {}". format(os.path.join(TenxApp.config['TENX_SCRIPTS_PATH'], 'blah.jinja'))):
            TenxApp.load_script_template('blah')

        script_template = TenxApp.load_script_template('foo')
        self.assertIsNotNone(script_template)

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
