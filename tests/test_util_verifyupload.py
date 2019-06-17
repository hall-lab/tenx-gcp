#!/usrbin/env python

import os, subprocess, unittest
from mock import patch

from .context import tenx
from tenx import util

class VerifyUploadTest(unittest.TestCase):

    expected_remote = {
        'gatk-4.0.0.0.zip': '379508875',
        'longranger-2.2.2.tgz': '490894203',
        'loupe-2.1.1.tar.gz': '65286620',
        'supernova-2.0.1.tgz': '852601404',
        'supernova-2.1.1.tgz': '1314506272',
        'perl/verify-upload.pl': '2005',
        'objects,': 'TOTAL:'
    }

    gsutil_success_output = """
 379508875  2019-02-19T21:50:30Z  gs://data/gatk-4.0.0.0.zip
 490894203  2019-01-24T00:20:19Z  gs://data/longranger-2.2.2.tgz
  65286620  2019-03-07T20:27:34Z  gs://data/loupe-2.1.1.tar.gz
 852601404  2018-10-02T22:13:33Z  gs://data/supernova-2.0.1.tgz
1314506272  2018-10-02T22:08:59Z  gs://data/supernova-2.1.1.tgz
      2005  2018-06-26T18:15:58Z  gs://data/perl/verify-upload.pl
           TOTAL: 6 objects, 3102799379 bytes (2.89 GiB)

"""

    gsutil_missing_output = """
 490894203  2019-01-24T00:20:19Z  gs://data/longranger-2.2.2.tgz
  65286620  2019-03-07T20:27:34Z  gs://data/loupe-2.1.1.tar.gz
 852601404  2018-10-02T22:13:33Z  gs://data/supernova-2.0.1.tgz
1314506272  2018-10-02T22:08:59Z  gs://data/supernova-2.1.1.tgz
      2005  2018-06-26T18:15:58Z  gs://data/perl/verify-upload.pl
           TOTAL: 5 objects, 2723290504 bytes (2.89 GiB)

"""

    @patch('subprocess.check_output')
    def test1_build_remote(self, test_patch):
        test_patch.return_value = self.gsutil_success_output
        remote = util.build_remote(rurl="gs://data")
        self.assertDictEqual(self.expected_remote, remote)

    @patch('subprocess.check_output')
    def test2_empty(self, test_patch):
        test_patch.return_value = self.gsutil_success_output
        with self.assertRaisesRegex(Exception, "Local directory does not contain any files!"):
            util.verify_upload(ldir=os.path.join("tests", "test_util_verifyupload", "empty"), rurl="gs://data")

    @patch('subprocess.check_output')
    def test3_missing(self, test_patch):
        test_patch.return_value = self.gsutil_missing_output
        with self.assertRaisesRegex(Exception, "Remote is missing these files:\ngatk-4.0.0.0.zip"):
            util.verify_upload(ldir=os.path.join("tests", "test_util_verifyupload", "success"), rurl="gs://data")

    @patch('subprocess.check_output')
    def test4_success(self, test_patch):
        test_patch.return_value = self.gsutil_success_output
        util.verify_upload(ldir=os.path.join("tests", "test_util_verifyupload", "success"), rurl="gs://data")

    @patch('subprocess.check_output')
    def test5_ignored(self, test_patch):
        test_patch.return_value = self.gsutil_missing_output
        util.verify_upload(ldir=os.path.join("tests", "test_util_verifyupload", "success"), rurl="gs://data", ignore="gatk")

#-- VerifyUploadTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
