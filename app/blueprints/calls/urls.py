from flask import render_template, request, jsonify, abort, send_file

from app import session
from app.app_config import AppConfig
from calls import Uploader, UploadFile
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
        return send_file(upload.filepath)

    @blueprint.route('/fields')
    def get_aggregated_field():
        """Return the requested field as a file"""
        aggregateQuery = request.args
        return jsonify({})