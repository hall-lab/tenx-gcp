import filecmp, io, json, os, subprocess, sys, tempfile, unittest
from click.testing import CliRunner
from mock import call, patch
import socket

#from tenx.cli import cli
from tenx.aln_cli import tenx_aln_cli as cli
from tenx.aln_pipeline import aln_pipeline_cmd, run_pipeline
import tenx.app, tenx.notifications
from tenx.alignment import TenxAlignment
from tenx.sample import TenxSample
from tenx.reference import TenxReference

class AlnPipelineTest(unittest.TestCase):
    
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        sample = TenxSample(name="__SAMPLE__", base_path=self.temp_d.name)
        ref = TenxReference(name="__REF__")
        self.aln = sample.alignment(ref=ref)
        os.makedirs(os.path.join(self.aln.path))
        tenx.app.TenxApp.config = {
            "TENX_DATA_PATH": os.path.join(self.temp_d.name),
            "TENX_REMOTE_URL": "gs://data",
            "TENX_REMOTE_REFSU_URL": "gs://resources/refs",
            "TENX_CROMWELL_PATH": os.path.join(os.path.dirname(__file__), "data", "app"),
        }

    def tearDown(self):
        self.temp_d.cleanup()
        tenx.app.TenxApp.config = None

    @patch("socket.gethostname")
    @patch("tenx.notifications.slack")
    @patch("subprocess.check_call")
    def test_aln_pipeline(self, subprocess_check_call_p, notifications_p, hostname_p):
        runner = CliRunner()
        hostname_p.return_value = "deven"

        result = runner.invoke(cli, ["pipeline", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(aln_pipeline_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(aln_pipeline_cmd, [self.aln.sample.name, self.aln.ref.name])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertEqual(hostname_p.call_count, 2)
        notifications_p.assert_has_calls([
            call("{} ALN START deven".format(self.aln.sample.name, self.aln.ref.name)),
            call("{} ALN SUCCESS deven".format(self.aln.sample.name, self.aln.ref.name))
            ])
        subprocess_check_call_p.assert_called_once()

    @patch("subprocess.check_call")
    def test_run_pipeline(self, subprocess_check_call_p):
        s = io.StringIO()
        sys.stderr = s
        aln = TenxSample(name="blah", base_path=self.temp_d.name).assembly()
        run_pipeline(self.aln)
        subprocess_check_call_p.assert_called_once()
        self.assertRegex(s.getvalue(), "RUNNING: java -Dconfig.file")
        sys.stderr = sys.__stderr__

# -- AlnPipelineTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
