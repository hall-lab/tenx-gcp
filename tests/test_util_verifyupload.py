import os, shutil, subprocess, tempfile, unittest
from mock import patch

from .context import tenx
from tenx import util

class VerifyUploadTest(unittest.TestCase):

    expected_remote = {
        "file1": "12",
        "file2": "12",
        "dir1/file3": "12",
        "dir2/file4": "12",
        "objects,": "TOTAL:",
    }

    gsutil_success_output = """
12  2019-02-19T21:50:30Z  gs://data/file1
12  2019-01-24T00:20:19Z  gs://data/file2
12  2019-03-07T20:27:34Z  gs://data/dir1/file3
12  2018-10-02T22:13:33Z  gs://data/dir2/file4
           TOTAL: 4 objects, 3102799379 bytes (48 B)

    """

    gsutil_missing_output = """
12  2019-02-19T21:50:30Z  gs://data/file1
12  2019-01-24T00:20:19Z  gs://data/file2
12  2019-03-07T20:27:34Z  gs://data/dir1/file3
           TOTAL: 3 objects, 3102799379 bytes (48 B)
"""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.empty_dir = os.path.join(self.tempdir, "empty")
        os.mkdir(self.empty_dir)
        self.success_dir = os.path.join(self.tempdir, "success")
        os.makedirs(self.success_dir)
        for bn in self.expected_remote.keys():
            fn = os.path.join(self.success_dir, bn)
            if not os.path.exists(os.path.dirname(fn)):
                os.makedirs( os.path.dirname(fn) )
            with open(fn, "w") as f: f.write("A")

    def tearDown(self):
        shutil.rmtree(self.tempdir)

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
        with self.assertRaisesRegex(Exception, "Remote is missing these files:\ndir2/file4"):
            util.verify_upload(ldir=self.success_dir, rurl="gs://data")

    @patch('subprocess.check_output')
    def test4_success(self, test_patch):
        test_patch.return_value = self.gsutil_success_output
        util.verify_upload(ldir=self.success_dir, rurl="gs://data")

    @patch('subprocess.check_output')
    def test5_ignored(self, test_patch):
        test_patch.return_value = self.gsutil_missing_output
        util.verify_upload(ldir=self.success_dir, rurl="gs://data", ignore="dir2")

#-- VerifyUploadTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
