from pathlib import Path

from models import Upload

class UploadPathManager:
    """Manages path functionality for call uploads"""
    FILENAME_FORMAT = '%I_%M_%P'

    def __init__(self, basePath):
        self.basePath = Path(basePath)

    def _get_path(self, upload):
        """Return the path for an upload record"""
        if not isinstance(upload, Upload):
            raise ValueError("Can only get path for Upload records")

        if not upload.id: #checking id also ensures it has a ts
            raise ValueError("Upload record not yet flushed or committed, cannot get path")
        uploadedTs = upload.ts_uploaded
        pathParts = map(str, [uploadedTs.year, uploadedTs.month, uploadedTs.day])
        path = self.basePath.joinpath('/'.join(pathParts))
        return path

    def _get_filename(self, upload, extension):
        """Return the name for an upload"""
        if not isinstance(upload, Upload):
            raise ValueError("Can only create a filename for Upload records")

        if not upload.ts_uploaded:
            raise ValueError("Upload record not yet flushed or committed, cannot get filename")
        return upload.ts_uploaded.strftime(f"{UploadPathManager.FILENAME_FORMAT}_{upload.id}.{extension}")

    def get_abs_path(self, upload, extension):
        """Return the absolute path for this upload"""
        filename = self._get_filename(upload, extension)
        filePath = self._get_path(upload)
        return str(filePath.joinpath(filename))