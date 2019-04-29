#!/usrbin/env python

import os
import subprocess
import tempfile
import unittest

class RunDurationTest(unittest.TestCase):

    def test_success(self):
        try:
            os.chdir('run-duration-t')
            out = subprocess.check_output(["python", "../../scripts/common/run-duration.py", "../run-duration-t"])
            self.assertEqual(out, "\nHours:      46.0\nJobs:       34\nMem:        276\nThreads:    38\nCore Hours: 50.0\n")
        finally:
            os.chdir('..')

#-- RunDurationTest

if __name__ == '__main__':
    unittest.main()
