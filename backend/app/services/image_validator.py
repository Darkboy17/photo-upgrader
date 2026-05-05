from fastapi import UploadFile

from app.core.config import get_settings
from app.core.errors import BadImageError


class ImageValidator:
    def __init__(self):
        self.settings = get_settings()

    async def validate_upload(self, file: UploadFile) -> bytes:
        if not file.content_type:
            raise BadImageError("Missing file content type.")

        if file.content_type not in self.settings.allowed_types_list:
            raise BadImageError(
                f"Unsupported file type: {file.content_type}. "
                f"Allowed types: {', '.join(self.settings.allowed_types_list)}"
            )

        data = await file.read()

        if not data:
            raise BadImageError("Uploaded file is empty.")

        if len(data) > self.settings.max_upload_bytes:
            raise BadImageError(
                f"File too large. Maximum allowed size is {self.settings.max_upload_mb}MB."
            )

        return data
