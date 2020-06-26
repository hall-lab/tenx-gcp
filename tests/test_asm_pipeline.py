import filecmp, io, json, os, subprocess, sys, tempfile, unittest
from click.testing import CliRunner
from mock import call, patch
import socket

from tenx.asm_pipeline import asm_pipeline_cmd, run_pipeline
import tenx.app, tenx.notifications
from tenx.sample import TenxSample

class AsmPipelineTest(unittest.TestCase):
    
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        sample = TenxSample(name="__SAMPLE__", base_path=self.temp_d.name)
        self.asm = sample.assembly()
        os.makedirs(os.path.join(self.asm.path))
        tenx.app.TenxApp.config = {
            "TENX_DATA_PATH": os.path.join(self.temp_d.name, "__SAMPLE__", "assembly"),
            "TENX_REMOTE_URL": "gs://data",
            "TENX_CROMWELL_PATH": os.path.join(os.path.dirname(__file__), "data", "app"),
        }

    def tearDown(self):
        self.temp_d.cleanup()
        tenx.app.TenxApp.config = None

    @patch("socket.gethostname")
    @patch("tenx.notifications.slack")
    @patch("subprocess.check_call")
    def test_asm_pipeline(self, subprocess_check_call_p, notifications_p, hostname_p):
        runner = CliRunner()
        result = runner.invoke(asm_pipeline_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_pipeline_cmd, [])
        self.assertEqual(result.exit_code, 2)

        hostname_p.return_value = "deven"

        result = runner.invoke(asm_pipeline_cmd, [self.asm.sample.name])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        hostname_p.assert_called_once()
        notifications_p.assert_has_calls([call("{} START deven".format(self.asm.sample.name)), call("{} SUCCESS deven".format(self.asm.sample.name))])
        subprocess_check_call_p.assert_called_once()

    @patch("subprocess.check_call")
    def test_run_pipeline(self, subprocess_check_call_p):
        s = io.StringIO()
        sys.stderr = s
        asm = TenxSample(name="blah", base_path=self.temp_d.name).assembly()
        run_pipeline(self.asm)
        subprocess_check_call_p.assert_called_once()
        self.assertRegex(s.getvalue(), "RUNNING: java -Dconfig.file")
        sys.stderr = sys.__stderr__

# -- AsmPipelineTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
