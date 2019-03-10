from flask import url_for


class UploadJson:
    """Represent an Upload record as a json"""
    def __init__(self, upload):
        self.upload = upload

    def __call__(self):
        """Return the upload as json"""
        if not self.upload.id: #not yet flushed / available for client
            return {}
        id = self.upload.id
        ts = self.upload.ts_uploaded.isoformat()
        filename = self.upload.source_filename
        downloadUrl = url_for('calls.download_upload', idUpload=self.upload.id)
        return {
            'id': id,
            'ts': ts,
            'filename': filename,
            'downloadUrl': downloadUrl
        }