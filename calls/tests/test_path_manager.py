from unittest import TestCase
from unittest.mock import Mock

from models import Upload

from ..upload_path_manager import UploadPathManager


class test_get_path(TestCase):
    """Test cases for the get_path method"""

    def test_with_non_upload(self):
        """Attempting to get a path with a non-Upload record should raise an error"""
        testCaseObject = UploadPathManager()
        nonUploadRecord = Mock()
        with self.assertRaises(ValueError):
            result = testCaseObject.get_path(nonUploadRecord)

    def test_without_id(self):
        """Attempting to get a path without an ID should raise an error"""
        testCaseObject = UploadPathManager()
        uploadWithNoId = Upload()
        with self.assertRaises(ValueError):
            result = testCaseObject.get_path(uploadWithNoId)
