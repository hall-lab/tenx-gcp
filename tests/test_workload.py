import filecmp, os, re, StringIO, sys, tempfile, unittest
from mock import patch

from .context import tenx
from tenx import workload

class TenxJobTest(unittest.TestCase):

    def test1_job(self):
        job = workload.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)

    def test2_template(self):
        templates_p = workload.Job.templates_path()
        self.assertRegexpMatches(templates_p, re.compile("tenx\/job\-templates"))

        job = workload.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)
        self.assertRegexpMatches(job.template_fn(), re.compile("aln-pipeline.sbatch.sh$"))

        template = job.load_template()
        self.assertIsNotNone(template)

    @patch('subprocess.check_call')
    def test3_script(self, check_call_patch):
        job = workload.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)

        script_f = tempfile.NamedTemporaryFile()
        job.write_script(params={"SAMPLE_NAME": "__SAMPLE__", "REF_NAME": "__REF__"}, script_fn=script_f.name)
        self.assertTrue( filecmp.cmp(script_f.name, os.path.join("tests", "test_workload", "aln-pipeline.sbatch.sh")) )

        check_call_patch.return_value = '0'
        err = StringIO.StringIO()
        sys.stderr = err
        job.launch_script(params={"SAMPLE_NAME": "__SAMPLE__", "REF_NAME": "__REF__"})
        self.assertRegexpMatches(err.getvalue(), re.compile("RUNNING: sbatch \/tmp"))
        sys.stderr = sys.__stderr__

# -- TenxJobTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
