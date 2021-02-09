import os, sys, tempfile, unittest, yaml
from mock import patch

from tenx.app import TenxApp, TenxCromwell
from tenx.reference import TenxReference
from tenx.sample import TenxSample

class TenxAppTest1(unittest.TestCase):

    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "app")
        self.temp_d = tempfile.TemporaryDirectory()
        self.sample = TenxSample(name="__TEST__", base_path=self.temp_d.name)
        self.asm = self.sample.assembly()
        self.ref = TenxReference(name="__REF__")
        self.aln = self.sample.alignment(ref=self.ref)
        TenxApp.config = None

    def tearDown(self):
        TenxApp.config = None
        self.temp_d.cleanup()

    def test_init_fails(self):
        if TenxApp.config is None: TenxApp()
        TenxApp.config = None
        with self.assertRaisesRegex(IOError, "No such file or directory"):
            TenxApp("/tenx.yaml")

    def test_init(self):
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

    def test_cromwell_fails(self):
        with self.assertRaisesRegex(Exception, "Tenx config has not been initialized!"):
            cromwell = TenxCromwell(entity=self.asm)

        TenxApp.config = { "TENX_CROMWELL_PATH": "/", }
        with self.assertRaisesRegex(Exception, "Cromwell jar not found at /cromwell.jar!"):
            cromwell = TenxCromwell(entity=self.asm)

        with self.assertRaisesRegex(Exception, "Unknown entity:"):
            cromwell = TenxCromwell(entity=self.sample)

    def test_cromwell(self):
        TenxApp.config = { "TENX_CROMWELL_PATH": self.data_dn, }

        ref = TenxReference(name="__REF__")
        test_params = [
                {
                    "pipeline": "supernova",
                    "entity": self.asm,
                    "inputs": {"SAMPLE_NAME": self.asm.sample.name},
                },
                {
                    "pipeline": "longranger",
                    "entity": self.aln,
                    "inputs": {"SAMPLE_NAME": self.aln.sample.name, "REF_NAME": self.aln.ref.name},
                },
                ]
        for p in test_params:
            pipeline_name = p["pipeline"]
            entity = p["entity"]
            cromwell = TenxCromwell(entity=entity)
            self.assertTrue(cromwell)
            self.assertEqual(cromwell.entity, entity)
            self.assertEqual(cromwell.pipeline_name, pipeline_name)

            templates_dn = cromwell.templates_dn
            self.assertTrue(templates_dn)

            cromwell_dn = cromwell.cromwell_dn
            self.assertEqual(cromwell_dn, TenxApp.config.get("TENX_CROMWELL_PATH"))
            self.assertEqual(cromwell.cromwell_jar, os.path.join(cromwell_dn, "cromwell.jar"))

            inputs_bn = ".".join([pipeline_name, "inputs", "json"])
            self.assertEqual(cromwell.inputs_bn, inputs_bn)
            wdl_bn = ".".join([pipeline_name, "gcloud", "wdl"])
            self.assertEqual(cromwell.wdl_bn, wdl_bn)
            conf_bn = ".".join([pipeline_name, "conf"])
            self.assertEqual(cromwell.conf_bn, conf_bn)

            self.assertDictEqual(cromwell.inputs_for_entity(), p["inputs"])

            conf_fn = os.path.join(cromwell.pipeline_dn, conf_bn)
            inputs_fn = os.path.join(cromwell.pipeline_dn, inputs_bn)
            wdl_fn = os.path.join(cromwell.pipeline_dn, wdl_bn)

            cmd = cromwell.command()
            expected_cmd = ["java", "-Dconfig={}".format(conf_fn), "-jar", cromwell.cromwell_jar, wdl_fn, "-i", inputs_fn]

            self.assertTrue(os.path.exists(conf_fn))
            self.assertTrue(os.path.exists(inputs_fn))
            self.assertTrue(os.path.exists(wdl_fn))

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
        with self.assertRaisesRegex(Exception, "Scripts directory \(TENX_SCRIPTS_PATH\) is not set in tenx config!"):
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
