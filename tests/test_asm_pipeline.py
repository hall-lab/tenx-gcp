import os, tempfile, unittest
from click.testing import CliRunner
from mock import call, patch
import socket

from tenx.asm_pipeline import asm_pipeline_cmd
import tenx.app, tenx.assembly, tenx.asm_upload, tenx.notifications, tenx.reads

class AsmPipelineTest(unittest.TestCase):
    
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.makedirs(os.path.join(self.temp_d.name, "__SAMPLE__", "assembly"))
        tenx.app.TenxApp.config = {
            "TENX_DATA_PATH": self.temp_d.name,
            "TENX_REMOTE_URL": "gs://data",
        }

    def tearDown(self):
        self.temp_d.cleanup()
        tenx.app.TenxApp.config = None

    @patch("socket.gethostname")
    @patch("tenx.notifications.slack")
    @patch("tenx.reads.download")
    @patch("tenx.assembly.run_assemble")
    @patch("tenx.assembly.run_mkoutput")
    @patch("tenx.asm_upload.run_upload")
    def test2_asm_pipeline(self, asm_upload_p, asm_mkoutput_p, asm_assemble_p, reads_dl_p, notifications_p, hostname_p):
        runner = CliRunner()
        result = runner.invoke(asm_pipeline_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_pipeline_cmd, [])
        self.assertEqual(result.exit_code, 2)

        hostname_p.return_value = "deven"

        result = runner.invoke(asm_pipeline_cmd, ["__SAMPLE__"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        hostname_p.assert_called_once()
        notifications_p.assert_has_calls([call("__SAMPLE__ START deven"), call("__SAMPLE__ SUCCESS deven")])
        reads_dl_p.assert_called_once()
        asm_assemble_p.assert_called_once()
        asm_mkoutput_p.assert_called_once()
        asm_upload_p.assert_called_once()

# -- AsmPipelineTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
#notifications.slack("{} START {}".format(sample_name, socket.gethostname()))
#reads.download(reads.TenxReads(sample_name=sample_name))
#asm = assembly.TenxAssembly(sample_name=sample_name)
#assembly.run_assemble(asm)
#assembly.run_mkoutput(asm)
#run_upload(asm, assembly.TenxAssembly(sample_name=sample_name, base_path=TenxApp.config["TENX_REMOTE_URL"]))
#notifications.slack("{} FAILED {}".format(sample_name, socket.gethostname()))
#notifications.slack("{} SUCCESS {}".format(sample_name, socket.gethostname()))
