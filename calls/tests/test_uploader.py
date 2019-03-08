from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock

from ..exc import InvalidExtension
from ..uploader import Uploader

class test_upload(TestCase):
    """Tests for the upload method"""

    def test_with_invalid_extension(self):
        """A file object with no extension is not allowed"""
        sessionMock = Mock()
        testPath = '/test/path'
        testCase = Uploader(sessionMock, testPath)

        fileMock = Mock(filename='test')
        with self.assertRaises(InvalidExtension):
            testCase.upload(fileMock)

    def test_with_invalid_extension(self):
        """A file object with an invalid extension is not allowed"""
        sessionMock = Mock()
        testPath = '/test/path'
        testCase = Uploader(sessionMock, testPath)

        fileMock = Mock(filename='test.test')
        with self.assertRaises(InvalidExtension):
            testCase.upload(fileMock)

