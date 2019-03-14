import random
import statistics

from unittest import TestCase
from unittest.mock import Mock, patch

from calls.wrappers import AggregateField
from models import Upload

from ..aggregate_mean import get_aggregate_mean


class ChunkWithMean:
    """A stub with expected interface that the get_aggregate_mean function expects"""
    def __init__(self, value, count):
        self.value = value
        self.count = count

    def __getitem__(self, item):
        """Implement item getting interface"""
        return self

    def __len__(self):
        """Implement the len method"""
        return self.count

    def mean(self):
        """Implement the mean() interface"""
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


class test_get_aggregate_mean(TestCase):
    """Test cases for the get_aggregate_mean function"""

    def test_with_same_values(self):
        """Method should return the value even if the vals are all the same"""
        upload = Upload()

        testField = AggregateField(*['test'])

        count = 5
        sameVals = [10 for i in range(count)]
        mockedReturnVals = [ChunkWithMean(v, count) for v in sameVals]

        with patch('calls.aggregate.functions.aggregate_mean.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals
            result = get_aggregate_mean(upload, testField)
            self.assertEqual(result, statistics.mean(sameVals))

    def test_with_different_values(self):
        """Method should return the mean value given a list of random ints"""
        upload = Upload()
        testField = AggregateField(*['test'])

        count = 100
        randomVals = [random.choice([i for i in range(count)]) for i in range(count)]
        mockedReturnVals = [ChunkWithMean(v, count) for v in randomVals]

        with patch('calls.aggregate.functions.aggregate_mean.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals
            result = get_aggregate_mean(upload, testField)
            self.assertEqual(result, statistics.mean(randomVals))

    def test_with_different_counts(self):
        """Method should return the correct value even with diff population sizes"""
        upload = Upload()
        testField = AggregateField(*['test'])

        count = 100
        randomVals = [random.choice([i for i in range(count)]) for i in range(count)]
        mockedReturnVals = [ChunkWithMean(v, random.choice([i for i in range(count)])) for v in randomVals]

        weights = [chunkWithMean.value * chunkWithMean.count for chunkWithMean in mockedReturnVals]
        expectedMean = sum(weights) / sum(chunkWithMean.count for chunkWithMean in mockedReturnVals)

        with patch('calls.aggregate.functions.aggregate_mean.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals
            result = get_aggregate_mean(upload, testField)
            self.assertEqual(result, expectedMean)