from models import Upload

class UploadPathManager:
    """Manages path functionality for call uploads"""

    def get_path(self, upload):
        """Return the path for an upload record"""
        if not isinstance(upload, Upload):
            raise ValueError("Can only get path for Upload records")

        if not upload.id:
            raise ValueError("Upload record not yet flushed or committed, cannot get path")