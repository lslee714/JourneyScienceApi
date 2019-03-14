import numpy as np

from utils import chunkify_big_json

from .get_nested_chunk import get_nested_chunk


def get_aggregate_min(upload, aggregateField):
    """Get the min of the aggregate field for this upload"""
    value = None
    chunks = chunkify_big_json(upload.filepath)
    for chunk in chunks:
        try:
            chunkMember = get_nested_chunk(chunk, aggregateField)
        except (KeyError, IndexError): #skip ones that arent applicable for the query
            continue
        chunkMember.replace('', np.NaN, inplace=True)
        chunkMember.dropna(inplace=True)
        try:
            series = chunkMember.apply(float)
            chunkVal = float(series.min())
        except ValueError:
            series = chunkMember
            chunkVal = series.min()

        if chunkVal is None:
            continue
        if value is None:
            value = chunkVal
        elif value > chunkVal:
            value = chunkVal
    return value
