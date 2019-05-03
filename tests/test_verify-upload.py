#!/usrbin/env python

import os, subprocess, sys, tempfile, unittest
from mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/common')))
from verify_upload import build_remote, run
from pprint import pprint

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
    def test_build_remote(self, test_patch):
        test_patch.return_value = self.gsutil_success_output
        remote = build_remote(rurl="gs://data")
        self.assertDictEqual(self.expected_remote, remote)

    @patch('subprocess.check_output')
    def test_empty(self, test_patch):
        test_patch.return_value = self.gsutil_success_output
        with self.assertRaises(Exception) as cm:
            run(ldir="verify-upload-t/empty", rurl="gs://data")
        self.assertTrue("No files found in verify-upload-t/empty/" in cm.exception)

    @patch('subprocess.check_output')
    def test_missing(self, test_patch):
        test_patch.return_value = self.gsutil_missing_output
        with self.assertRaises(Exception) as cm:
            run(ldir="verify-upload-t/success", rurl="gs://data")
        self.assertTrue("Remote is missing these files:\ngatk-4.0.0.0.zip" in cm.exception)

    @patch('subprocess.check_output')
    def test_success(self, test_patch):
        test_patch.return_value = self.gsutil_success_output
        run(ldir="verify-upload-t/success", rurl="gs://data")

#-- VerifyUploadTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
