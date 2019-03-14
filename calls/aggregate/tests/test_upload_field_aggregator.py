from unittest import TestCase

from models import Upload

from calls.exc import UnknownOperation

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
        expectedMatchingMethod = testAggregator.get_min

        method = testAggregator.get_method_for_operation(implementedOperation)
        self.assertEqual(method, expectedMatchingMethod)


#Not testing the get_min/max_mean methods as those are trivial proxies to the aggregate min/max/mean functions with an added call
