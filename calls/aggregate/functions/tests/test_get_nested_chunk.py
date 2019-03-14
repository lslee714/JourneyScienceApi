from unittest import TestCase
from unittest.mock import patch

from calls.wrappers import AggregateField

from ..get_nested_chunk import get_nested_chunk

class ChunkStub:
    """Stub class to use for get_nested_chunk"""
    def __init__(self, value):
        self.value = value

    def apply(self, val):
        return self

    def __getitem__(self, val):
        return ChunkStub(self.value[val])

    def __eq__(self, other):
        return str(self.value) == other


class test_get_nested_chunk(TestCase):
    """Test cases for get_nested_chunk"""

    def test_with_no_field_names_and_no_position(self):
        """Given an aggregate field with only a name, method should return the corresponding value """
        query = 'testA'
        testChunkStub = {
            query: 'foo',
            'testB': 'foo'
        }
        aggregateField = AggregateField(query)

        result = get_nested_chunk(testChunkStub, aggregateField)
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
        aggregateField = AggregateField(*queryArgs)

        result = get_nested_chunk(testChunkStub, aggregateField)
        expectedVal = testChunkStub[queryArgs[0]][correspondingPosition]
        self.assertEqual(result, expectedVal)

    def test_with_only_nested_fields(self):
        """Given an aggregate field with only additional nested fields, should return the corresponding value"""
        queryArgs = ['testA', 'testAnestedVal', 'hi']
        desiredValue = 'bye'

        testChunkStub = ChunkStub({
            'testA': {'testAnestedVal': {'hi': desiredValue}},
            'testB': 'foo'
        })

        aggregateField = AggregateField(*queryArgs)

        result = get_nested_chunk(testChunkStub, aggregateField)
        self.assertEqual(result, desiredValue)

    def test_with_nested_fields_and_position(self):
        """Given an aggregate field with both additional nested fields and position,
         should return the corresponding key value for the position"""
        queryArgs = ['testA', '2', 'testAnestedVal', 'anotherLayer']
        desiredValue = 'find me!'

        testChunkStub = ChunkStub({
            'testA': [{'testAnestedVal': {'anotherLayer': 'dont find me'}},
                      {'testAnestedVal': {'anotherLayer': desiredValue}},
                      {'testAnestedVal': {'anotherLayer': 'dont find me'}}],
            'testB': 'foo'
        })
        aggregateField = AggregateField(*queryArgs)

        with patch('calls.aggregate.functions.get_nested_chunk.pd.Series') as seriesPatch:
            seriesPatchChunk = testChunkStub[aggregateField.name][aggregateField.position]
            seriesPatch.return_value = seriesPatchChunk
            result = get_nested_chunk(testChunkStub, aggregateField)
            self.assertEqual(result, desiredValue)