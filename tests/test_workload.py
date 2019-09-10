import unittest

from .context import tenx
from tenx import workload

class TenxJobTest(unittest.TestCase):

    def test10_job(self):
        job = workload.Job(name="test", manager="slurm")

# -- TenxJobTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
