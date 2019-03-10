from models import Upload

from utils import chunkify_big_json

class UploadFieldAggregator:
    """Given a field, returns a json of an aggregate function of that field requested Uploads """

    def __init__(self, uploads):
        self.uploads = uploads

    def aggregate(self, field, operation):
        """Aggregate the field"""
        operationMap = {
            'min': self.get_aggregate_min,
            'max': self.get_aggregate_max,
            'mean': self.get_aggregate_mean
        }
        operation = operationMap[operation]
        return operation(field)

    def _get_min_max(self, field, op):
        """Common functionality between aggregating min/max"""
        value = None
        for upload in self.uploads:
            chunks = chunkify_big_json(upload.filepath)
            for chunk in chunks:
                chunkVal = getattr(chunk[field], op)()
                if value is None or value > chunkVal:
                    value = chunkVal
        return value

    def get_aggregate_min(self, field):
        """Get the aggregate min"""
        return self._get_min_max(field, 'min')

    def get_aggregate_max(self, field):
        """Get the aggregate max"""
        return self._get_min_max(field, 'max')

    def get_aggregate_mean(self, field):
        """Get the aggregate mean"""
        meansToWeight = {}
        for upload in self.uploads:
            uploadMeans = []
            chunks = chunkify_big_json(upload.filepath)
            for chunk in chunks:
                chunkVal = chunk[field].mean()
                uploadMeans.append(chunkVal)
