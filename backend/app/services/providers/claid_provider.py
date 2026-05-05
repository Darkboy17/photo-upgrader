import json

import httpx

from app.core.config import get_settings
from app.core.errors import ProviderError
from app.services.providers.base import ImageEnhancementProvider


class ClaidProvider(ImageEnhancementProvider):
    def __init__(self):
        self.settings = get_settings()
        self.url = "https://api.claid.ai/v1/image/edit/upload"

    async def enhance(self, image_bytes: bytes) -> bytes:
        if not self.settings.claid_api_key:
            raise ProviderError("CLAID_API_KEY is missing.")

        headers = {
            "Authorization": f"Bearer {self.settings.claid_api_key}",
        }

        operations_payload = {
            "operations": {
                "restorations": {
                    "decompress": "auto",
                    "upscale": "smart_enhance",
                    "polish": True,
                },
                "resizing": {
                    "width": "200%",
                    "height": "200%",
                    "fit": "bounds",
                },
                "background": {
                    "remove": {
                        "category": "products",
                        "clipping": False,
                    },
                    "color": "#ffffff",
                },
                "adjustments": {
                    "hdr": {
                        "intensity": 100,
                        "stitching": False,
                    },
                    "exposure": 5,
                    "saturation": 5,
                    "contrast": 8,
                    "sharpness": 15,
                },
                "padding": "8%",
            },
            "output": {
                "format": {
                    "type": "png",
                    "compression": "optimal",
                }
            },
        }

        files = {
            "file": ("product.png", image_bytes, "image/png"),
            "data": (
                None,
                json.dumps(operations_payload),
                "application/json",
            ),
        }

        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(
                self.url,
                headers=headers,
                files=files,
            )

        if response.status_code >= 400:
            raise ProviderError(
                f"Claid provider failed: {response.status_code} {response.text[:800]}"
            )

        payload = response.json()
        tmp_url = (
            payload.get("data", {})
            .get("output", {})
            .get("tmp_url")
        )

        if not tmp_url:
            raise ProviderError(
                f"Claid did not return output tmp_url: {payload}")

        async with httpx.AsyncClient(timeout=120) as client:
            image_response = await client.get(tmp_url)

        if image_response.status_code >= 400:
            raise ProviderError(
                f"Failed to download Claid output: {image_response.status_code}"
            )

        return image_response.content
