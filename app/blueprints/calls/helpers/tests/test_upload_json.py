from datetime import datetime
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
        upload = Upload(id=id, ts_uploaded=ts)
        uploadJson = UploadJson(upload)

        expectedResult = {
            'id': id,
            'ts': ts.isoformat()
        }
        self.assertEqual(uploadJson(), expectedResult)
