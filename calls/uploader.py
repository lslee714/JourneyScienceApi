from pathlib import Path

from .exc import InvalidExtension
from .upload_path_manager import UploadPathManager


class Uploader:
    """Uploads calls"""
    SUPPORTED_EXTENSIONS = frozenset({'gz', 'zip'})

    def __init__(self, basePath):
        self.pathManager = UploadPathManager(basePath)

    def upload(self, uploadFile):
        """Create, upload and return the fileObject"""
        if not uploadFile.extension or (uploadFile.extension and uploadFile.extension not in self.SUPPORTED_EXTENSIONS):
            raise InvalidExtension("Cannot upload, invalid/supported extension.")

        uploadFilePath = self.pathManager.get_abs_path(uploadFile)
        uploadFilePath.mkdir(parents=True, exist_ok=True)
        with open(uploadFilePath, 'wb') as uploadWriteFile:
            uploadWriteFile.write(uploadFile.fileObj)