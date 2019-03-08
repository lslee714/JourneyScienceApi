from pathlib import Path

from .exc import InvalidExtension
from .upload_path_manager import UploadPathManager


class Uploader:
    """Uploads calls"""
    SUPPORTED_EXTENSIONS = frozenset({'gz', 'zip'})

    def __init__(self, session, basePath):
        self.session = session
        self.pathManager = UploadPathManager(basePath)

    def upload(self, fileObj):
        """Create and upload the fileObject"""
        fileObjPath = Path(fileObj.filename)
        extension = fileObjPath.suffix.lstrip('.')
        if not extension:
            raise InvalidExtension("No extension specified, cannot upload")
        elif extension and extension not in self.SUPPORTED_EXTENSIONS:
            raise InvalidExtension("Unsupported extension, cannot upload")
