import asyncio

import httpx

from app.core.config import get_settings
from app.core.errors import ProviderError
from app.services.providers.base import ImageEnhancementProvider


class StabilityRelightProvider(ImageEnhancementProvider):
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.stability.ai/v2beta/stable-image"

    async def enhance(self, image_bytes: bytes) -> bytes:
        if not self.settings.stability_api_key:
            raise ProviderError("STABILITY_API_KEY is missing.")

        generation_id = await self._start_relight_job(image_bytes)
        return await self._poll_result(generation_id)

    async def _start_relight_job(self, image_bytes: bytes) -> str:
        url = f"{self.base_url}/edit/replace-background-and-relight"

        headers = {
            "Authorization": f"Bearer {self.settings.stability_api_key}",
            "Accept": "application/json",
        }

        files = {
            "subject_image": ("subject.png", image_bytes, "image/png"),
        }

        data = {
            "background_prompt": (
                "clean white seamless studio background, premium ecommerce product photography, "
                "soft realistic shadow, commercial catalog lighting"
            ),
            "foreground_prompt": (
                "preserve the exact same product, same shape, same color, same material, "
                "same logo, same design, sharp realistic details"
            ),
            "negative_prompt": (
                "different product, changed logo, changed shape, changed color, extra objects, "
                "people, hands, watermark, text, distorted, duplicate product, blurry"
            ),
            "preserve_original_subject": "0.85",
            "light_source_direction": "above",
            "light_source_strength": "0.35",
            "output_format": "png",
        }

        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(url, headers=headers, files=files, data=data)

        if response.status_code >= 400:
            raise ProviderError(
                f"Stability relight start failed: {response.status_code} {response.text[:500]}"
            )

        payload = response.json()
        generation_id = payload.get("id")

        if not generation_id:
            raise ProviderError(f"Stability did not return an id: {payload}")

        return generation_id

    async def _poll_result(self, generation_id: str) -> bytes:
        url = f"{self.base_url}/results/{generation_id}"

        headers = {
            "Authorization": f"Bearer {self.settings.stability_api_key}",
            "Accept": "image/*",
        }

        async with httpx.AsyncClient(timeout=180) as client:
            for _ in range(60):
                response = await client.get(url, headers=headers)

                if response.status_code == 202:
                    await asyncio.sleep(2)
                    continue

                if response.status_code >= 400:
                    raise ProviderError(
                        f"Stability result polling failed: {response.status_code} {response.text[:500]}"
                    )

                content_type = response.headers.get("content-type", "")

                if "image" not in content_type:
                    raise ProviderError(
                        f"Stability returned non-image result: {response.text[:500]}"
                    )

                return response.content

        raise ProviderError("Stability relight job timed out while polling results.")