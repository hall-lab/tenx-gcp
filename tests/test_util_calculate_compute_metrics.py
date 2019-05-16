import datetime, os, subprocess, tempfile, unittest

from .context import tenx
from tenx import util

class TenxUtilCalculateComputeMetricsTest(unittest.TestCase):

    def test_failures(self):
        with self.assertRaisesRegexp(OSError, 'No such file or directory'):
            util.calculate_compute_metrics('/blah')

        with self.assertRaisesRegexp(Exception, 'Failed to find log path ending'):
            util.calculate_compute_metrics('tests')

    def test_success(self):
        metrics = util.calculate_compute_metrics(os.path.join('tests', 'test_util_calculate_compute_metrics'))
        expected_metrics = {
            'directory': 'tests/test_util_calculate_compute_metrics',
            'jobs':       34,
            'mem':        276,
            'threads':    38,
            'core_hours': 50.0,
            'duration':   datetime.timedelta(1, 78434, 494619),
        }
        self.assertDictEqual(metrics, expected_metrics)

#-- TenxUtilTest

if __name__ == '__main__':
    unittest.main()

#-- main
