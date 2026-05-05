import httpx

from app.core.config import get_settings
from app.core.errors import ProviderError
from app.services.providers.base import ImageEnhancementProvider


class HuggingFaceProvider(ImageEnhancementProvider):
    def __init__(self):
        self.settings = get_settings()

    async def enhance(self, image_bytes: bytes) -> bytes:
        if not self.settings.hf_api_token:
            raise ProviderError("HF_API_TOKEN is missing.")

        url = f"https://api-inference.huggingface.co/models/{self.settings.hf_model}"

        headers = {
            "Authorization": f"Bearer {self.settings.hf_api_token}",
            "Content-Type": "image/png",
        }

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, headers=headers, content=image_bytes)

        if response.status_code >= 400:
            raise ProviderError(
                f"Hugging Face provider failed: {response.status_code} {response.text[:300]}"
            )

        content_type = response.headers.get("content-type", "")

        if "image" not in content_type:
            raise ProviderError(
                f"Hugging Face returned non-image response: {response.text[:300]}")

        return response.content
