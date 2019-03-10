class InvalidExtension(Exception):
    """Error to raise when a file is trying to be uploaded that's not supported"""

class UnknownOperation(Exception):
    """Error for an unknown/unimplemented operation"""

class AggregationFailed(Exception):
    """Error to raise when failing to aggregate"""