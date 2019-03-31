from celery.states import FAILURE, SUCCESS, PENDING, STARTED
from flask import render_template, request, jsonify, abort, send_from_directory, url_for
from pathlib import Path

from app import session
from app.async import aggregate
from app.app_config import AppConfig
from calls import Uploader, UploadFile, UploadFieldAggregator
from calls.wrappers import AggregateField
from models import Upload

from .helpers import UploadJson

def register(blueprint):
    """Register the routes for the blueprint"""
    @blueprint.route('/')
    def index():
        """Main page for the phone calls blueprint"""
        return render_template('calls/index.html')

    @blueprint.route('/', methods=['POST'])
    def create_upload():
        """Create a new Upload record and upload it appropriately"""
        fileStorage = request.files['file']
        uploader = Uploader(AppConfig.BASE_UPLOAD_PATH)
        newUpload = Upload(source_filename=fileStorage.filename)
        uploadFile = UploadFile(newUpload, fileStorage)
        if uploader.can_upload(uploadFile):
            session.add(newUpload)
            session.flush() #Give uploader access to id/ts
            uploader.upload(uploadFile)
            session.commit()
            return jsonify({})
        else:
            return jsonify({'error': 'Failed to upload, please ensure the file is uploadable'}), 500

    @blueprint.route('/uploads')
    def retrieve_uploads():
        """Send the current uploads to the client"""
        uploads = session.query(Upload).order_by(Upload.ts_uploaded.desc()).all()
        return jsonify({'data': [UploadJson(upload)() for upload in uploads]})

    @blueprint.route('/uploads/<idUpload>')
    def download_upload(idUpload):
        """Download the upload"""
        upload = session.query(Upload).get(idUpload)
        if not upload:
            abort(404)
        filePath = Path(upload.filepath)
        return send_from_directory(filePath.parent, filePath.name, as_attachment=True,
                         attachment_filename=upload.source_filename)

    @blueprint.route('/fields')
    def get_aggregated_field():
        """Return the aggregated field from the upload(s)"""
        aggregateQuery = request.args
        operationQuery = aggregateQuery['aggregate']
        fieldQuery = aggregateQuery['field'].strip()
        uploadIdsQuery = aggregateQuery.getlist('uploads')
        uploadsToAggregate = session.query(Upload).filter(Upload.id.in_(uploadIdsQuery))
        aggregator = UploadFieldAggregator(uploadsToAggregate)

        aggregateFieldArgs = [queryArg.strip() for queryArg in fieldQuery.split(',')]
        aggregateField = AggregateField(*aggregateFieldArgs)
        aggregatedValue = aggregator.aggregate(aggregateField, operationQuery)
        return jsonify({'data': f'The {operationQuery} of {fieldQuery} for uploads\
            with ID {", ".join(uploadIdsQuery)} is {aggregatedValue}'})

    @blueprint.route('/fields/async')
    def get_aggregated_field_async():
        """Return the requested field as a file"""
        aggregateQuery = request.args
        operationQuery = aggregateQuery['aggregate']
        fieldQuery = aggregateQuery['field'].strip()
        uploadIdsQuery = aggregateQuery.getlist('uploads')
        aggregateFieldArgs = [queryArg.strip() for queryArg in fieldQuery.split(',')]
        aggregatedValue = aggregate.apply_async(args=[uploadIdsQuery, operationQuery, *aggregateFieldArgs])
        return jsonify({'statusUrl': url_for('.get_aggregate_status', idTask=aggregatedValue.id)}), 202

    @blueprint.route('/tasks/<idTask>')
    def get_aggregate_status(idTask):
        task = aggregate.AsyncResult(idTask)
        if task.state == SUCCESS:
            httpCode = 200
            resultArg = dict(data=task.result.get('message'))
        elif task.state in [PENDING, STARTED]:
            httpCode = 102
            resultArg = dict(data=None)
        else: #assume something went wrong
            httpCode = 500
            resultArg = dict(error=str(task.result))
        return jsonify({'state': task.state, **resultArg}), httpCode