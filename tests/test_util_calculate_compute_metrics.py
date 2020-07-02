import datetime, os, unittest

import tenx.util as util

class TenxUtilCalculateComputeMetricsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "test_util_calculate_compute_metrics")

    def test_failures(self):
        with self.assertRaisesRegex(Exception, 'Cannot compute compute metrics! Run directory'):
            util.calculate_compute_metrics('/BLAH')

        with self.assertRaisesRegex(Exception, "Failed to find log path ending in '_CS'"):
            util.calculate_compute_metrics(os.path.dirname(self.data_dn))

    def test_success(self):
        metrics_d = self.data_dn
        metrics = util.calculate_compute_metrics(metrics_d)
        expected_metrics = {
            'directory': metrics_d,
            'jobs':       34,
            'mem':        276,
            'threads':    38,
            'core_hours': 50.0,
            'duration':   datetime.timedelta(1, 78434, 494619),
        }
        self.assertDictEqual(metrics, expected_metrics)

#-- TenxUtilTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- main
