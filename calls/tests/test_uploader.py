from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock

from models import Upload

from ..exc import InvalidExtension
from ..uploader import Uploader
from ..wrappers import UploadFile

class test_upload(TestCase):
    """Tests for the upload method"""

    def test_with_no_extension(self):
        """A file object with no extension is not allowed"""
        testPath = '/test/path'
        testCase = Uploader(testPath)

        upload = Upload()
        mockFileObj = Mock(filename='test')

        uploadFile = UploadFile(upload, mockFileObj)
        with self.assertRaises(InvalidExtension):
            testCase.upload(uploadFile)

    def test_with_unsupported_extension(self):
        """A file object with an unsupported extension is not allowed"""
        testPath = '/test/path'
        testCase = Uploader(testPath)

        upload = Upload()
        mockFileObj = Mock(filename='test')

        uploadFile = UploadFile(upload, mockFileObj)

        with self.assertRaises(InvalidExtension):
            testCase.upload(uploadFile)

