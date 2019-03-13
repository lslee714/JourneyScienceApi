from celery.states import FAILURE
from celery.exceptions import CeleryError

from app import celery, session
from calls import UploadFieldAggregator
from calls.exc import AggregationFailed
from calls.wrappers import AggregateField
from models import Upload

@celery.task(bind=True)
def aggregate(self, uploadIds, operationQuery, *aggregateArgs):
    """Background task that runs a long function with progress reports."""

    uploads = session.query(Upload).filter(Upload.id.in_(uploadIds)).all()
    uploadAggregator = UploadFieldAggregator(uploads)
    aggregateField = AggregateField(*aggregateArgs)
    try:
        aggregatedValue = uploadAggregator.aggregate(aggregateField, operationQuery)
    except AggregationFailed as e:
        self.update_state(state=FAILURE, meta={'status': 'Aggregation failed',
                                                'result': str(e)})


    return {'status': 'Aggregation completed!',
            'result': aggregatedValue}
