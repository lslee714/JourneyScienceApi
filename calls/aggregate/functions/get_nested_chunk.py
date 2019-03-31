from copy import copy
import pandas as pd


def get_nested_chunk(chunk, aggregateField):
    """Given an AggregateField, return the nested chunk(series) that matches the aggregate query"""

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
