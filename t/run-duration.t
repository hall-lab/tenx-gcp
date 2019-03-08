#!/usrbin/env python

import os
import subprocess
import tempfile
import unittest

class RunDurationTest(unittest.TestCase):

    def test_success(self):
        rv = subprocess.call(["python", "../tenx-scripts/run-duration.py"])
        self.assertEqual(rv, 1)

    def test_success(self):
        file, fname = tempfile.mkstemp()
        print(fname)
        try:
            os.chdir('run-duration-t')
            out = subprocess.check_output(["python", "../../tenx-scripts/run-duration.py"])
            self.assertEqual(out, "\nHours:      46.0\nJobs:       34\nMem:        276\nThreads:    38\nCore Hours: 50.0\n")
        finally:
            os.chdir('..')
            #os.remove(fname)

    # run-duration
#

if __name__ == '__main__':
    unittest.main()
