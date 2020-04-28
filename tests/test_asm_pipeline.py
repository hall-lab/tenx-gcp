import unittest
from click.testing import CliRunner

from tenx.asm_pipeline import asm_pipeline_cmd

class AsmPipelineTest(unittest.TestCase):

    def test2_tenx_assembly_pipeline(self):
        runner = CliRunner()
        result = runner.invoke(asm_pipeline_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_pipeline_cmd, [])
        self.assertEqual(result.exit_code, 2)

# -- AsmPipelineTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
