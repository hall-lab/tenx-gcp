import filecmp, os, re, tempfile, unittest

from .context import tenx
from tenx import workload

class TenxJobTest(unittest.TestCase):

    def test1_job(self):
        job = workload.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)

    def test2_template(self):
        job = workload.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)
        self.assertRegexpMatches(job.template_fn(), re.compile("aln-pipeline.sbatch.sh$"))

        template = job.load_template()
        self.assertIsNotNone(template)

        script_f = tempfile.NamedTemporaryFile()
        job.write_script(params={"SAMPLE_NAME": "__SAMPLE__", "REF_NAME": "__REF__"}, script_fn=script_f.name)
        self.assertTrue( filecmp.cmp(script_f.name, os.path.join("tests", "test_workload", "aln-pipeline.sbatch.sh")) )

# -- TenxJobTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
