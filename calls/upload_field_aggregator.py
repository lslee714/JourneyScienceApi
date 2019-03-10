from models import Upload


class UploadFieldAggregator:
    """Given a field, returns a json of an aggregate of that field for all Uploads """

    def aggregate(self, field):
        """Aggregate the field"""