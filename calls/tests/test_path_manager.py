from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from models import Upload

from ..upload_path_manager import UploadPathManager


TEST_BASE_PATH = '/test/path'
TEST_EXTENSION = 'test'

class test_get_abs_path(TestCase):
    """Test cases for the get_abs_path method"""

    def test_with_non_upload(self):
        """Attempting to get a path with a non-Upload record should raise an error"""
        pathManager = UploadPathManager(TEST_BASE_PATH)
        nonUploadRecord = Mock()
        with self.assertRaises(ValueError):
            result = pathManager.get_abs_path(nonUploadRecord, TEST_EXTENSION)

    def test_without_id(self):
        """Attempting to get a path without an ID should raise an error"""
        pathManager = UploadPathManager(TEST_BASE_PATH)
        uploadWithNoId = Upload()
        with self.assertRaises(ValueError):
            result = pathManager.get_abs_path(uploadWithNoId, TEST_EXTENSION)


    def test_without_ts(self):
        """Attempting to get a path without a timestamp should raise an error"""
        pathManager = UploadPathManager(TEST_BASE_PATH)
        uploadWithNoTs = Upload(id='test', ts_uploaded=None)
        with self.assertRaises(ValueError):
            result = pathManager.get_abs_path(uploadWithNoTs, TEST_EXTENSION)

    def test_valid_upload(self):
        """Given a valid upload record, should return the expected filename"""
        testUploadTs = datetime.now()
        validUpload = Upload(id=1, ts_uploaded=testUploadTs)

        expectedResult = f"{TEST_BASE_PATH}/{testUploadTs.year}/{testUploadTs.month}/{testUploadTs.day}/" + \
            f"{testUploadTs.strftime(UploadPathManager.FILENAME_FORMAT)}_{validUpload.id}.{TEST_EXTENSION}"


        result = UploadPathManager(TEST_BASE_PATH).get_abs_path(validUpload, TEST_EXTENSION)
        self.assertEqual(result, expectedResult)
