import random

from unittest import TestCase
from unittest.mock import patch, Mock

from models import Upload

from ..exc import UnknownOperation
from ..upload_field_aggregator import UploadFieldAggregator

class test_get_method_for_operation(TestCase):
    """Test cases for the get_method_for_operation test case"""

    def test_with_unknown_operaton(self):
        """An unknown operation should raise an UnknownOperation error"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        unknownOperation = 'stdev'

        with self.assertRaises(UnknownOperation):
            testAggregator.get_method_for_operation(unknownOperation)

    def test_with_known_operation(self):
        """An implemented operation should return the associated method"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        implementedOperation= 'min'
        expectedMatchingMethod = testAggregator.get_aggregate_min

        method = testAggregator.get_method_for_operation(implementedOperation)
        self.assertEqual(method, expectedMatchingMethod)


class ChunkWithMinMax:
    """A stub with expected interface that the get_aggregate_min/max methods expects"""
    def __init__(self, value):
        self.value = value

    def __getitem__(self, item):
        """Implement item getting interface"""
        return self

    def min(self):
        """Implement the min() interface"""
        return self.value

    def max(self):
        """Implement the max() interface"""
        return self.value


class test_get_aggregate_min(TestCase):
    """Test cases for the get_aggregate_min method"""

    def test_with_same_values(self):
        """Method should return the value even if the vals are all the same"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = 'test'

        sameVals = [0 for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in sameVals]

        with patch('calls.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals
            result = testAggregator.get_aggregate_min(testField)
            self.assertEqual(result, min(sameVals))

    def test_with_different_values(self):
        """Method should return the min value given a list of random ints"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = 'test'

        randomVals = [random.choice([i for i in range(5)]) for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in randomVals]

        with patch('calls.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals
            result = testAggregator.get_aggregate_min(testField)
            self.assertEqual(result, min(randomVals))

class test_get_aggregate_max(TestCase):
    """Test cases for the get_aggregate_max method"""

    def test_with_same_values(self):
        """Method should return the value even if the vals are all the same"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = 'test'

        sameVals = [0 for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in sameVals]

        with patch('calls.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals

            result = testAggregator.get_aggregate_max(testField)
            self.assertEqual(result, max(sameVals))

    def test_with_different_values(self):
        """Method should return the min value given a list of random ints"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = 'test'

        randomVals = [random.choice([i for i in range(5)]) for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in randomVals]

        with patch('calls.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals

            result = testAggregator.get_aggregate_max(testField)
            self.assertEqual(result, max(randomVals))