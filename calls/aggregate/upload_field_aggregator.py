import statistics

from calls.exc import UnknownOperation

from .functions import get_aggregate_max, get_aggregate_min, get_aggregate_mean

class UploadFieldAggregator:
    """Given a AggregateField, returns a json of an aggregate function of that field requested Uploads """
    MIN_OPERATION = 'min'
    MAX_OPERATION = 'max'
    MEAN_OPERATION = 'mean'

    def __init__(self, uploads):
        self.uploads = uploads

    def get_method_for_operation(self, operation):
        """Return the associated method for the operation"""
        operationMap = {
            self.MIN_OPERATION: self.get_min,
            self.MAX_OPERATION: self.get_max,
            self.MEAN_OPERATION: self.get_mean
        }
        if operation not in operationMap:
            raise UnknownOperation(f"Requested operation {operation} unknown/not implemented.")
        return operationMap[operation]

    def aggregate(self, aggregateField, operation):
        """Aggregate the field"""
        method = self.get_method_for_operation(operation)
        return method(aggregateField)

    def get_min(self, aggregateField):
        """Get the aggregate min"""
        values = []
        for upload in self.uploads:
            values.append(get_aggregate_min(upload, aggregateField))
        return min(values)

    def get_max(self, aggregateField):
        """Get the aggregate max"""
        values = []
        for upload in self.uploads:
            values.append(get_aggregate_max(upload, aggregateField))
        return max(values)

    def get_mean(self, aggregateField):
        """Get the aggregate mean"""
        allMeans = []
        for upload in self.uploads:
            allMeans.append(get_aggregate_mean(upload, aggregateField))

        return statistics.mean(allMeans)