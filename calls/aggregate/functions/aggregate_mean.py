import numpy as np

from calls.exc import AggregationFailed
from utils import chunkify_big_json

from .get_nested_chunk import get_nested_chunk


def get_aggregate_mean(upload, aggregateField):
    """Get the aggregate mean"""
    chunkMeanWeights = []
    chunks = chunkify_big_json(upload.filepath)
    items = 0
    for chunk in chunks:
        try:
            chunkMember = get_nested_chunk(chunk, aggregateField)
        except (KeyError, IndexError):  # skip ones that arent applicable for the query
            continue

        chunkMember.replace('', np.NaN, inplace=True)
        chunkMember.dropna(inplace=True)
        try:
            series = chunkMember.apply(float)
        except ValueError:
            raise AggregationFailed('Cannot get mean for requested query')

        items += len(series)
        chunkMeanWeight = series.mean() * len(series)
        chunkMeanWeights.append(chunkMeanWeight)
    if not chunkMeanWeights or not items > 0:
        raise AggregationFailed("Something went wrong, please verify your query.")

    #return the weighted mean
    return sum(chunkMeanWeights) / items
