import random

from unittest import TestCase
from unittest.mock import patch, MagicMock

from models import Upload

from calls.exc import UnknownOperation
from calls.wrappers import AggregateField

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

    def replace(self, *args, **kwargs):
        """Implement the replace() interface"""
        return self

    def dropna(self, *args, **kwargs):
        """Implement the dropna() interface"""
        return self

    def apply(self, *args, **kwargs):
        """Implement the apply interface"""
        return self

class test_get_aggregate_min(TestCase):
    """Test cases for the get_aggregate_min method"""

    def test_with_same_values(self):
        """Method should return the value even if the vals are all the same"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = AggregateField(*['test'])

        sameVals = [0 for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in sameVals]

        with patch('calls.aggregate.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals
            result = testAggregator.get_aggregate_min(testField)
            self.assertEqual(result, min(sameVals))

    def test_with_different_values(self):
        """Method should return the min value given a list of random ints"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = AggregateField(*['test'])

        randomVals = [random.choice([i for i in range(5)]) for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in randomVals]

        with patch('calls.aggregate.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals
            result = testAggregator.get_aggregate_min(testField)
            self.assertEqual(result, min(randomVals))

class test_get_aggregate_max(TestCase):
    """Test cases for the get_aggregate_max method"""

    def test_with_same_values(self):
        """Method should return the value even if the vals are all the same"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = AggregateField(*['test'])

        sameVals = [0 for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in sameVals]

        with patch('calls.aggregate.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals

            result = testAggregator.get_aggregate_max(testField)
            self.assertEqual(result, max(sameVals))

    def test_with_different_values(self):
        """Method should return the min value given a list of random ints"""
        uploads = [Upload() for i in range(5)]
        testAggregator = UploadFieldAggregator(uploads)

        testField = AggregateField(*['test'])

        randomVals = [random.choice([i for i in range(5)]) for i in range(5)]
        mockedReturnVals = [ChunkWithMinMax(v) for v in randomVals]

        with patch('calls.aggregate.upload_field_aggregator.chunkify_big_json') as chunkFnMock:
            chunkFnMock.return_value = mockedReturnVals

            result = testAggregator.get_aggregate_max(testField)
            self.assertEqual(result, max(randomVals))


class test_get_chunk_member(TestCase):
    """Test cases for get_chunk_member"""

    def test_with_no_field_names_and_no_position(self):
        """Given an aggregate field with only a name, method should return the corresponding value """
        query = 'testA'
        testChunkStub = {
            query: 'foo',
            'testB': 'foo'
        }
        uploads = [Upload() for i in range(5)]
        aggregateField = AggregateField(query)

        aggregator = UploadFieldAggregator(uploads)

        result = aggregator.get_chunk_member(testChunkStub, aggregateField)
        expectedVal = testChunkStub[query]
        self.assertEqual(result, expectedVal)

    def test_with_only_position(self):
        """Given an aggregate field with a position, method should return the corresponding value for the key"""
        queryArgs = ['testA', '1']
        correspondingPosition = int(queryArgs[1]) - 1 #aggregate field accounts for 0 based indexing
        testChunkStub = {
            'testA': ['foo', 'bar', 'hello', 'world'],
            'testB': 'foo'
        }
        uploads = [Upload() for i in range(5)]
        aggregator = UploadFieldAggregator(uploads)
        aggregateField = AggregateField(*queryArgs)

        result = aggregator.get_chunk_member(testChunkStub, aggregateField)
        expectedVal = testChunkStub[queryArgs[0]][correspondingPosition]
        self.assertEqual(result, expectedVal)

    def test_with_only_nested_fields(self):
        """Given an aggregate field with only additional nested fields, should return the corresponding value"""
        queryArgs = ['testA', 'testAnestedVal']
        testChunkStub = MagicMock(return_value={
            'testA': {'testAnestedVal': 'hi'},
            'testB': 'foo'
        })
        #Ignore pandas structure changes
        testChunkStub.__getitem__.return_value.apply.return_value = testChunkStub.__getitem__.return_value

        uploads = [Upload() for i in range(5)]
        aggregator = UploadFieldAggregator(uploads)
        aggregateField = AggregateField(*queryArgs)

        result = aggregator.get_chunk_member(testChunkStub, aggregateField)
        expectedVal = testChunkStub[queryArgs[0]][queryArgs[1]]
        self.assertEqual(result, expectedVal)

    def test_with_nested_fields_and_position(self):
        """Given an aggregate field with both additional nested fields and position,
         should return the corresponding key value for the position"""
        queryArgs = ['testA', '2', 'testAnestedVal', 'anotherLayer']
        desiredValue = 'find me!'
        testChunkStub = MagicMock(return_value= {
            'testA': [{'testAnestedVal': {'anotherLayer': 'dont find me'}},
                      {'testAnestedVal': {'anotherLayer': desiredValue}},
                      {'testAnestedVal': {'anotherLayer': 'dont find me'}}],
            'testB': 'foo'
        })

        aggregateField = AggregateField(*queryArgs)
        uploads = [Upload() for i in range(5)]

        with patch('calls.aggregate.upload_field_aggregator.pd.Series') as seriesPatch:
            seriesApplyMock = MagicMock()
            seriesPatch.return_value.apply = seriesApplyMock

            aggregator = UploadFieldAggregator(uploads)

            result = aggregator.get_chunk_member(testChunkStub, aggregateField)
            seriesApplyMock.assert_called_with(seriesPatch)
            for nestedField in aggregateField.nested_fields:
                seriesApplyMock.return_value.__getitem__.assert_called()