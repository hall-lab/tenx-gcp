import subprocess, unittest
from click.testing import CliRunner

from tenx.asm_cli import tenx_asm_cli,  asm_assemble,  asm_mkoutput,  asm_pipeline,  asm_rm_asm_files_cmd,  asm_upload

class TenxAsmCliTest(unittest.TestCase):

    def test1_tenx_assembly(self):
        runner = CliRunner()
        result = runner.invoke(tenx_asm_cli, [])
        self.assertEqual(result.exit_code, 0)

    def test2_tenx_assembly_assemble(self):
        runner = CliRunner()
        result = runner.invoke(asm_assemble, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_assemble, [])
        self.assertEqual(result.exit_code, 2)

    def test2_tenx_assembly_pipeline(self):
        runner = CliRunner()
        result = runner.invoke(asm_pipeline, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_pipeline, [])
        self.assertEqual(result.exit_code, 2)

    def test2_tenx_assembly_mkoutput(self):
        runner = CliRunner()
        result = runner.invoke(asm_mkoutput, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_mkoutput, [])
        self.assertEqual(result.exit_code, 2)

    def test2_tenx_assembly_rm_asm_files_cmd(self):
        runner = CliRunner()
        result = runner.invoke(asm_rm_asm_files_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_rm_asm_files_cmd, [])
        self.assertEqual(result.exit_code, 2)

    def test2_tenx_assembly_upload(self):
        runner = CliRunner()
        result = runner.invoke(asm_upload, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_upload, [])
        self.assertEqual(result.exit_code, 2)

# -- TenxAsmCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
