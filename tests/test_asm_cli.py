import subprocess, unittest
from click.testing import CliRunner
from mock import patch

import tenx.app, tenx.assembly
from tenx.asm_cli import tenx_asm_cli,  asm_assemble,  asm_mkoutput, asm_cleanup_cmd

class TenxAsmCliTest(unittest.TestCase):

    def setUp(self):
        tenx.app.TenxApp.config = { "TENX_DATA_PATH": "/mnt/disks/data" }

    def tearDown(self):
        tenx.app.TenxApp.config = None

    def test1_tenx_assembly(self):
        runner = CliRunner()
        result = runner.invoke(tenx_asm_cli, [])
        self.assertEqual(result.exit_code, 0)

    @patch("tenx.assembly.run_assemble")
    def test2_tenx_assembly_assemble(self, assemble_p):
        runner = CliRunner()
        result = runner.invoke(asm_assemble, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_assemble, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(asm_assemble, ["TEST"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = ""
        self.assertEqual(result.output, expected_output)

    def test2_tenx_assembly_mkoutput(self):
        runner = CliRunner()
        result = runner.invoke(asm_mkoutput, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_mkoutput, [])
        self.assertEqual(result.exit_code, 2)

    def test2_asm_cleanup_cmd(self):
        runner = CliRunner()
        result = runner.invoke(asm_cleanup_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_cleanup_cmd, [])
        self.assertEqual(result.exit_code, 2)

# -- TenxAsmCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
