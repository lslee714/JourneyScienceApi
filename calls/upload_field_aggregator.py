import numpy as np
import pandas as pd

from copy import copy
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
            raise UnknownOperation(f"Requested operation {operation} unknown/not implemented.")
        return operationMap[operation]

    def aggregate(self, aggregateField, operation):
        """Aggregate the field"""
        method = self.get_method_for_operation(operation)
        return method(aggregateField)

    def get_chunk_member(self, chunk, aggregateField):
        """Given an aggregate field, grab the associated member from the chunk"""

        #ASSUMES a
        #{ key: [ {}, {}... {} ] } or
        #{ key: {}...n} or
        #{key: val} structure
        #could make this a fancy recursive flattener,
        #but at that point would be obtrusive to UX
        #and probably better to rethink the data formatting/normalizing upstream

        mainFieldName = aggregateField.name
        if aggregateField.nested_fields and aggregateField.position is not None:
            subChunk = pd.Series(chunk[mainFieldName][aggregateField.position])
            nestedFields = copy(aggregateField.nested_fields)
            while nestedFields:
                topNestedName = nestedFields.pop(0)
                subChunk = subChunk.apply(pd.Series)[topNestedName]
            return subChunk

        elif aggregateField.nested_fields:
            subChunk = chunk[mainFieldName]
            aggregateFields = copy(aggregateField.nested_fields)
            while aggregateFields:
                topNestedName = aggregateFields.pop(0)
                subChunk = subChunk.apply(pd.Series)[topNestedName]
            return subChunk #last item will be value

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
                try:
                    chunkMember = self.get_chunk_member(chunk, aggregateField)
                except (KeyError, IndexError): #skip ones that arent applicable for the query
                    continue
                chunkMember.replace('', np.NaN, inplace=True)
                chunkMember.dropna(inplace=True)
                try:
                    series = chunkMember.apply(float)
                    chunkVal = float(getattr(series, op)())
                except ValueError:
                    series = chunkMember
                    chunkVal = getattr(series, op)()

                if chunkVal is None:
                    continue
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
