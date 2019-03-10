from datetime import datetime
from flask import url_for
from unittest import TestCase

from models import Upload

from ..upload_json import UploadJson


class test_call(TestCase):
    """Test cases of the __call__ method"""

    def test_with_non_flushed(self):
        """A non flushed upload should return a dictionary with empty values"""
        upload = Upload(id=None, ts_uploaded=None)
        uploadJson = UploadJson(upload)
        self.assertEqual(uploadJson(), {})

    def test_with_flushed(self):
        """A flushed and available upload should return its id and uploaded ts"""
        id = 1
        ts = datetime.now()
        filename = 'test.gz'
        upload = Upload(id=id, ts_uploaded=ts, source_filename=filename)
        uploadJson = UploadJson(upload)

        #Not ideal, but this is a unittest so remove flask integration dependency
        #I could hardcode or hack the test script more to get the app
        #but I "expect" url_for from flask to not be broken
        uploadJson = uploadJson().pop('downloadUrl')

        expectedResult = {
            'id': id,
            'ts': ts.isoformat(),
            'filename': filename,
        }
        self.assertEqual(uploadJson(), expectedResult)
