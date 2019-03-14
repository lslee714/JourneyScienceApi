import random

from unittest import TestCase
from unittest.mock import patch

from calls.wrappers import AggregateField
from models import Upload

from ..aggregate_max import get_aggregate_max


class ChunkWithMax:
    """A stub with expected interface that the get_aggregate_max methods expects"""
    def __init__(self, value):
        self.value = value

    def __getitem__(self, item):
        """Implement item getting interface"""
        return self

    def max(self):
        """Implement the max() interface"""
        return self.value

    def replace(self, *args, **kwargs):
        """Implement the replace() interface"""
        return self

    def dropna(self, *args, **kwargs):
        """Implement the dropna() interface"""
        return self

    def apply(self, *args, **kwargs):
        """Implement the apply interface"""
        return self


class test_get_aggregate_max(TestCase):
    """Test cases for get_aggregate_max function"""

    def test_with_same_values(self):
        """Method should return the value even if the vals are all the same"""
        upload = Upload()

        testField = AggregateField(*['test'])

        sameVals = [0 for i in range(5)]
        mockedReturnVals = [ChunkWithMax(v) for v in sameVals]

        with patch('calls.aggregate.functions.aggregate_max.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals

            result = get_aggregate_max(upload, testField)
            self.assertEqual(result, max(sameVals))

    def test_with_different_values(self):
        """Method should return the min value given a list of random ints"""
        upload = Upload()

        testField = AggregateField(*['test'])

        randomVals = [random.choice([i for i in range(5)]) for i in range(5)]
        mockedReturnVals = [ChunkWithMax(v) for v in randomVals]

        with patch('calls.aggregate.functions.aggregate_max.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals

            result = get_aggregate_max(upload, testField)
            self.assertEqual(result, max(randomVals))
