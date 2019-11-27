import io, os, re, sys, tempfile, unittest
from mock import patch

from .context import tenx
from tenx import compute

class TenxJobTest(unittest.TestCase):

    def test1_job(self):
        job = compute.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)

    def test2_template(self):
        templates_p = compute.Job.templates_path()
        self.assertRegex(templates_p, re.compile("tenx\/job\-templates"))

        job = compute.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)
        self.assertEqual(job.template_bn(), "aln-pipeline.slurm.sh")
        self.assertRegex(job.template_fn(), re.compile("aln-pipeline.slurm.sh$"))

        template = job.load_template()
        self.assertIsNotNone(template)

    @patch('subprocess.check_call')
    def test3_script(self, check_call_patch):
        job = compute.Job(name="aln-pipeline", manager="slurm")
        self.assertIsNotNone(job)

        with open(job.template_fn(), "r") as template_f:
            template = template_f.read()

        for s in ( "REF_NAME", "SAMPLE_NAME" ):
            s_re = re.compile("\{\{ " + s + " \}\}")
            template = re.sub(s_re, "___" + s + "___", template)

        s_re = re.compile("\{\{ TENX_DATA_PATH \}\}")
        template = re.sub(s_re, "", template)

        script_f = tempfile.NamedTemporaryFile()
        job.write_script(params={"SAMPLE_NAME": "___SAMPLE_NAME___", "REF_NAME": "___REF_NAME___"}, script_fn=script_f.name)

        script_f.flush()
        script_f.seek(0, 0)
        script = script_f.read()
        self.assertMultiLineEqual(script.decode(), template)
        
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err
        job.launch_script(params={"SAMPLE_NAME": "__SAMPLE__", "REF_NAME": "__REF__"})
        self.assertRegex(err.getvalue(), re.compile("RUNNING: sbatch \/tmp"))
        sys.stderr = sys.__stderr__

# -- TenxJobTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
