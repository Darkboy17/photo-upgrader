import httpx

from app.core.config import get_settings
from app.core.errors import ProviderError
from app.services.providers.base import ImageEnhancementProvider


class StabilityProvider(ImageEnhancementProvider):
    """
    Optional second provider.

    Stability API endpoints may change over time, so keep this isolated.
    Use this when you add a Stability API key and confirm the current endpoint
    from the official Stability API docs.
    """

    def __init__(self):
        self.settings = get_settings()

    async def enhance(self, image_bytes: bytes) -> bytes:
        if not self.settings.stability_api_key:
            raise ProviderError("STABILITY_API_KEY is missing.")

        url = "https://api.stability.ai/v2beta/stable-image/upscale/fast"

        headers = {
            "Authorization": f"Bearer {self.settings.stability_api_key}",
            "Accept": "image/*",
        }

        files = {
            "image": ("input.png", image_bytes, "image/png"),
        }

        data = {
            "output_format": "png",
        }

        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(url, headers=headers, files=files, data=data)

        if response.status_code >= 400:
            raise ProviderError(
                f"Stability provider failed: {response.status_code} {response.text[:300]}"
            )

        return response.content
