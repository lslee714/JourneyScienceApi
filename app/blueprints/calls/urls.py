from flask import render_template, request, jsonify

from app import db
from app.app_config import AppConfig
from calls import Uploader, UploadFile
from models import Upload

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
        newUpload = Upload()
        uploadFile = UploadFile(newUpload, fileStorage)
        if uploader.can_upload(uploadFile):
            db.session.add(newUpload)
            db.session.flush() #Give uploader access to id/ts
            uploader.upload(uploadFile)
            db.session.commit()
            return jsonify({})
        else:
            return jsonify({'error': 'Failed to upload, please ensure the file is uploadable'}), 500
