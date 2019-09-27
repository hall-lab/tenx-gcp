#!/usrbin/env python

import os, requests, unittest
from mock import patch

from .context import tenx
from tenx import notifications
from tenx.app import TenxApp

class NotificationsTest(unittest.TestCase):

    class Response(object):
        def __init__(self, ok):
            self.ok = ok

    @patch('requests.post')
    def test1_slack(self, test_patch):
        TenxApp()
        TenxApp.config['TENX_NOTIFICATIONS_SLACK'] = "https://slack.com"
        notok_response = NotificationsTest.Response(ok=False)
        test_patch.return_value = notok_response
        with self.assertRaisesRegexp(Exception, 'Slack POST failed for {}'.format(TenxApp.config['TENX_NOTIFICATIONS_SLACK'])):
            notifications.slack(message="Hello World!")

        ok_response = NotificationsTest.Response(ok=True)
        test_patch.return_value = ok_response
        notifications.slack(message="Hello World!")

#-- NotificationsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
