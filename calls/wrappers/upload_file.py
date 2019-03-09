from pathlib import Path

class UploadFile:
    """Wraps an Upload record with its file obj"""
    def __init__(self, upload, fileObj):
        self.upload = upload
        self.fileObj = fileObj

    @property
    def filename(self):
        """Return the filename associated w/ the file object"""
        return self.fileObj.filename

    @property
    def extension(self):
        """Return the extension associated w/ the file object"""
        return Path(self.filename).suffix.lstrip('.')