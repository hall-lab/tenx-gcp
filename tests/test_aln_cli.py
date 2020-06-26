import unittest
from click.testing import CliRunner

from tenx.aln_cli import tenx_aln_cli, aln_align, aln_pipeline, aln_upload

class AlnCliTest(unittest.TestCase):

    def test1_tenx_aln(self):
        runner = CliRunner()
        result = runner.invoke(tenx_aln_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(tenx_aln_cli, [])
        self.assertEqual(result.exit_code, 0)

    def test2_tenx_aln_align(self):
        runner = CliRunner()
        result = runner.invoke(aln_align, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(aln_align, [])
        self.assertEqual(result.exit_code, 2)

    def test2_tenx_aln_pipeline(self):
        runner = CliRunner()
        result = runner.invoke(aln_pipeline, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(aln_pipeline, [])
        self.assertEqual(result.exit_code, 2)

    def test2_tenx_aln_upload(self):
        runner = CliRunner()
        result = runner.invoke(aln_upload, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(aln_upload, [])
        self.assertEqual(result.exit_code, 2)

# -- AlnCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
