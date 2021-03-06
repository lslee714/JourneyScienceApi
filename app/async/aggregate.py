from celery.exceptions import Ignore
from celery.states import FAILURE

from app import celery, session
from calls import UploadFieldAggregator
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
        result = f'The {operationQuery} of {aggregateField.name} for uploads\
                    with ID {", ".join(uploadIds)} is {aggregatedValue}'
        return {'message': result}

    except Exception as e:
        self.update_state(state=FAILURE, meta={
            'exc_type': type(e).__name__,
            'exc_message': [str(e)]
        })
        raise Ignore()