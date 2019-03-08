from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from models import Upload

from ..upload_path_manager import UploadPathManager


TEST_BASE_PATH = '/test/path'
TEST_EXTENSION = 'test'

class test_get_path(TestCase):
    """Test cases for the get_path method"""

    def test_with_non_upload(self):
        """Attempting to get a path with a non-Upload record should raise an error"""
        pathManager = UploadPathManager(TEST_BASE_PATH)
        nonUploadRecord = Mock()
        with self.assertRaises(ValueError):
            result = pathManager.get_path(nonUploadRecord)

    def test_without_id(self):
        """Attempting to get a path without an ID should raise an error"""
        pathManager = UploadPathManager(TEST_BASE_PATH)
        uploadWithNoId = Upload()
        with self.assertRaises(ValueError):
            result = pathManager.get_path(uploadWithNoId)

    def test_with_valid_upload(self):
        """A valid upload should return the expected path"""
        pathManager = UploadPathManager(TEST_BASE_PATH)
        uploadedTs = datetime.now()
        validUpload = Upload(id=1, ts_uploaded=uploadedTs)

        EXPECTED_RESULT = f"{TEST_BASE_PATH}/{uploadedTs.year}/{uploadedTs.month}/{uploadedTs.day}"
        result = pathManager.get_path(validUpload)

        self.assertEqual(result, EXPECTED_RESULT)


class test_get_filename(TestCase):
    """Test cases for the get_filename static method"""

    def test_with_non_upload(self):
        """Cannot return a filename for a non Upload record"""
        nonUploadRecord = Mock()
        with self.assertRaises(ValueError):
            result = UploadPathManager.get_filename(nonUploadRecord, TEST_EXTENSION)

    def test_without_id(self):
        """Attempting to get a filename without a ts should raise an error"""
        uploadWithNoTs = Upload()
        with self.assertRaises(ValueError):
            result = UploadPathManager.get_filename(uploadWithNoTs, TEST_EXTENSION)

    def test_valid_upload(self):
        """Given a valid upload record, should return the expected filename"""
        testUploadTs = datetime.now()
        validUpload = Upload(id=1, ts_uploaded=testUploadTs)

        expectedResult = f"{testUploadTs.strftime(UploadPathManager.FILENAME_FORMAT)}_{validUpload.id}.{TEST_EXTENSION}"

        result = UploadPathManager.get_filename(validUpload, TEST_EXTENSION)
        self.assertEqual(result, expectedResult)
