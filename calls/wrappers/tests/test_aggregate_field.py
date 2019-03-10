from unittest import TestCase


from  ..aggregate_field import AggregateField


class test_nested_field(TestCase):
    """Test cases for the nested_field property"""

    def test_nested_fields_no_position(self):
        """The nested fields should return all the arguments"""
        query = ['test', 'test2', 'test3', 'test4']
        aggregateField = AggregateField(*query)
        for queryVal in query[1:]:
            self.assertIn(queryVal, aggregateField.nested_fields)

    def test_nested_fields_with_position(self):
        """Property should return all but the main and position argument values"""
        query = ['test', '2', 'test3', 'test4']
        aggregateField = AggregateField(*query)
        for queryVal in query[2:]:
            self.assertIn(queryVal, aggregateField.nested_fields)
        self.assertNotIn(query[1], aggregateField.nested_fields)

class test_position(TestCase):
    """Test cases for the position property"""

    def test_position_no_nested_fields(self):
        """The position should be returned and nested fields should be empty"""
        query = ['test', '1']
        expectedValue = 0 #property accounts for index based lists
        aggregateField = AggregateField(*query)
        self.assertEqual(aggregateField.position, expectedValue)
        self.assertEqual(len(aggregateField.nested_fields), 0)

    def test_position_with_nested_fields(self):
        """Property should return all but the main and position argument values"""
        query = ['test', '2', 'test3', 'test4']
        expectedPositionValue = 1
        aggregateField = AggregateField(*query)

        self.assertEqual(aggregateField.position, expectedPositionValue)

        self.assertNotIn(aggregateField.position, aggregateField.nested_fields)
        for queryVal in query[2:]:
            self.assertIn(queryVal, aggregateField.nested_fields)

