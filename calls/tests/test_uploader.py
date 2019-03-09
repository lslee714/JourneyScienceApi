from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch

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

    def test_with_valid_file(self):
        """An uploadable file should be written out to disk"""
        testPath = '/test/path'
        validUpload = Upload(id=1, ts_uploaded=datetime.now())
        uploadableMockFileObj = Mock(filename='test.gz')
        uploadFile = UploadFile(validUpload, uploadableMockFileObj)
        writeBinaryMode = 'wb'

        with patch('calls.uploader.UploadPathManager') as pathManagerMock:
            pathManagerMock.return_value.get_abs_path.return_value = uploadableMockFileObj
            with patch('calls.uploader.open') as openMock:
                enterMethodMock = Mock()
                openMock.return_value.__enter__ = enterMethodMock
                uploader = Uploader(testPath)
                uploader.upload(uploadFile)
                uploadableMockFileObj.mkdir.assert_called_with(exist_ok=True, parents=True)
                openMock.assert_called_with(uploadableMockFileObj, writeBinaryMode)
                enterMethodMock.return_value.write.assert_called_with(uploadFile.fileObj)