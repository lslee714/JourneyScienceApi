from utils import chunkify_big_json

from .exc import UnknownOperation

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
            self.MIN_OPERATION: self.get_aggregate_min,
            self.MAX_OPERATION: self.get_aggregate_max,
            self.MEAN_OPERATION: self.get_aggregate_mean
        }
        if operation not in operationMap:
            raise UnknownOperation(f"Requested operation {operation} unknown/not yet implemented.")
        return operationMap[operation]

    def aggregate(self, aggregateField, operation):
        """Aggregate the field"""
        method = self.get_method_for_operation(operation)
        return method(aggregateField)

    def get_chunk_member(self, chunk, aggregateField):
        """Given an aggregate field, grab the associated member from the chunk"""
        mainFieldName = aggregateField.name
        if aggregateField.nested_fields and aggregateField.position is not None:
            subChunk = chunk[mainFieldName][aggregateField.position]
            nestedFields = aggregateField.nested_fields
            while nestedFields:
                topNestedName = nestedFields.pop(0)
                subChunk = subChunk[topNestedName]
            return subChunk

        elif aggregateField.nested_fields:
            subChunk = chunk[mainFieldName]
            while aggregateField.nested_fields:
                topNestedName = aggregateField.nested_fields.pop(0)
                subChunk = subChunk[topNestedName]
            return subChunk

        elif aggregateField.position is not None:
            return chunk[mainFieldName][aggregateField.position]
        else:
            return chunk[mainFieldName]


    def _get_min_max(self, aggregateField, op):
        """Common functionality between aggregating min/max"""
        value = None
        for upload in self.uploads:
            chunks = chunkify_big_json(upload.filepath)
            for chunk in chunks:
                chunkMember= self.get_chunk_member(chunk, aggregateField)
                chunkVal = getattr(chunkMember, op)()
                if value is None:
                    value = chunkVal
                elif value > chunkVal and op == self.MIN_OPERATION:
                    value = chunkVal
                elif value < chunkVal and op == self.MAX_OPERATION:
                    value = chunkVal
        return value

    def get_aggregate_min(self, aggregateField):
        """Get the aggregate min"""
        return self._get_min_max(aggregateField, self.MIN_OPERATION)

    def get_aggregate_max(self, aggregateField):
        """Get the aggregate max"""
        return self._get_min_max(aggregateField, self.MAX_OPERATION)

    def get_aggregate_mean(self, aggregateField):
        """Get the aggregate mean"""
        meansToWeight = {}
        for upload in self.uploads:
            uploadMeans = []
            chunks = chunkify_big_json(upload.filepath)
            for chunk in chunks:
                chunkVal = chunk[aggregateField].mean()
                uploadMeans.append(chunkVal)
