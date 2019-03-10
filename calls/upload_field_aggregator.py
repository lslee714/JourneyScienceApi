from utils import chunkify_big_json

from .exc import UnknownOperation

class UploadFieldAggregator:
    """Given a field, returns a json of an aggregate function of that field requested Uploads """
    MIN_OPERATION = 'min'
    MAX_OPERATION = 'max'
    MEAN_OPERATION = 'mean'

    def __init__(self, uploads):
        self.uploads = uploads

    def get_method_for_operation(self, operation):
        """Return the associated method for the operation"""
        operationMap = {
            self.MIN_OPERATION: self.get_aggregate_min,
            self.MAX_OPERATION: self.get_aggregate_max,
            self.MEAN_OPERATION: self.get_aggregate_mean
        }
        if operation not in operationMap:
            raise UnknownOperation(f"Requested operation {operation} unknown/not yet implemented.")
        return operationMap[operation]

    def aggregate(self, field, operation):
        """Aggregate the field"""
        method = self.get_method_for_operation(operation)
        return method(field)

    def _get_min_max(self, field, op):
        """Common functionality between aggregating min/max"""
        value = None
        for upload in self.uploads:
            chunks = chunkify_big_json(upload.filepath)
            for chunk in chunks:
                chunkVal = getattr(chunk[field], op)()
                if value is None:
                    value = chunkVal
                elif value > chunkVal and op == self.MIN_OPERATION:
                    value = chunkVal
                elif value < chunkVal and op == self.MAX_OPERATION:
                    value = chunkVal
        return value

    def get_aggregate_min(self, field):
        """Get the aggregate min"""
        return self._get_min_max(field, self.MIN_OPERATION)

    def get_aggregate_max(self, field):
        """Get the aggregate max"""
        return self._get_min_max(field, self.MAX_OPERATION)

    def get_aggregate_mean(self, field):
        """Get the aggregate mean"""
        meansToWeight = {}
        for upload in self.uploads:
            uploadMeans = []
            chunks = chunkify_big_json(upload.filepath)
            for chunk in chunks:
                chunkVal = chunk[field].mean()
                uploadMeans.append(chunkVal)
