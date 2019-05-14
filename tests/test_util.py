import datetime, os, subprocess, tempfile, unittest

from .context import tenx
from tenx import util

class TenxUtilTest(unittest.TestCase):

    def test_run_duration(self):

        with self.assertRaisesRegexp(OSError, 'No such file or directory'):
            util.run_duration('/blah')

        with self.assertRaisesRegexp(Exception, 'Failed to find log path ending'):
            util.run_duration('tests')

        run = util.run_duration(os.path.join('tests', 'test_util_runduration'))
        expected_run = {
            'directory': 'tests/test_util_runduration',
            'jobs':       34,
            'mem':        276,
            'threads':    38,
            'core_hours': 50.0,
            'duration':   datetime.timedelta(1, 78434, 494619),
        }
        self.assertDictEqual(run, expected_run)

#-- TenxUtilTest

if __name__ == '__main__':
    unittest.main()

#-- main
