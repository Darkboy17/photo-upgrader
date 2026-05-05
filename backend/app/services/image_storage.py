import uuid
from pathlib import Path

import aiofiles

from app.core.config import get_settings


class ImageStorage:
    def __init__(self):
        self.settings = get_settings()
        self.input_dir = Path(self.settings.storage_input_dir)
        self.output_dir = Path(self.settings.storage_output_dir)
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def save_input(self, data: bytes, extension: str) -> tuple[str, str]:
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.{extension}"
        path = self.input_dir / filename

        async with aiofiles.open(path, "wb") as f:
            await f.write(data)

        return file_id, str(path)

    def output_path_for(self, job_id: str) -> str:
        return str(self.output_dir / f"{job_id}.png")

    def public_input_url(self, filename: str) -> str:
        return f"{self.settings.backend_base_url}/static/inputs/{filename}"

    def public_output_url(self, filename: str) -> str:
        return f"{self.settings.backend_base_url}/static/outputs/{filename}"
