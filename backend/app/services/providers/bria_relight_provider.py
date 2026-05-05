import asyncio
import base64
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.errors import ProviderError
from app.services.providers.base import ImageEnhancementProvider


class BriaRelightProvider(ImageEnhancementProvider):
    def __init__(self, light_type: str | None = None):
        self.settings = get_settings()
        self.base_url = "https://engine.prod.bria-api.com/v2/image/edit"
        self.light_type = light_type or self.settings.bria_light_type

    async def enhance(self, image_bytes: bytes) -> bytes:
        if not self.settings.bria_api_key:
            raise ProviderError("BRIA_API_KEY is missing.")

        request_id_or_payload = await self._start_relight(image_bytes)

        if isinstance(request_id_or_payload, bytes):
            return request_id_or_payload

        return await self._poll_result(request_id_or_payload)

    async def _start_relight(self, image_bytes: bytes) -> str | bytes:
        url = f"{self.base_url}/relight"

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_data_uri = f"data:image/png;base64,{image_base64}"

        headers = {
            "api_token": self.settings.bria_api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
            "image": image_data_uri,
            "light_type": self.light_type,
            "light_direction": self.settings.bria_light_direction,
        }

        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code >= 400:
            raise ProviderError(
                f"Bria relight start failed: {response.status_code} {response.text[:800]}"
            )

        content_type = response.headers.get("content-type", "")

        if "image" in content_type:
            return response.content

        data = response.json()

        request_id = self._extract_request_id(data)

        if not request_id:
            image_url = self._extract_image_url(data)
            if image_url:
                return await self._download_image(image_url)

            raise ProviderError(f"Bria did not return request id or image URL: {data}")

        return request_id

    async def _poll_result(self, request_id: str) -> bytes:
        """
        Bria v2 uses async processing/status service.
        If your Bria account/docs show a different status URL, only update this method.
        """
        candidate_urls = [
            f"https://engine.prod.bria-api.com/v2/status/{request_id}",
            f"https://engine.prod.bria-api.com/v2/result/{request_id}",
            f"https://engine.prod.bria-api.com/v2/results/{request_id}",
        ]

        headers = {
            "api_token": self.settings.bria_api_key,
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=180) as client:
            for _ in range(60):
                last_error: str | None = None

                for url in candidate_urls:
                    response = await client.get(url, headers=headers)

                    if response.status_code == 404:
                        last_error = response.text[:300]
                        continue

                    if response.status_code >= 400:
                        raise ProviderError(
                            f"Bria polling failed: {response.status_code} {response.text[:800]}"
                        )

                    content_type = response.headers.get("content-type", "")

                    if "image" in content_type:
                        return response.content

                    data = response.json()

                    status = str(
                        data.get("status")
                        or data.get("state")
                        or data.get("data", {}).get("status")
                        or ""
                    ).lower()

                    if status in {"queued", "pending", "processing", "running", "in_progress"}:
                        await asyncio.sleep(2)
                        break

                    if status in {"failed", "error"}:
                        raise ProviderError(f"Bria job failed: {data}")

                    image_url = self._extract_image_url(data)
                    if image_url:
                        return await self._download_image(image_url)

                    last_error = str(data)[:500]

                await asyncio.sleep(2)

        raise ProviderError("Bria relight job timed out while polling.")

    async def poll_existing_result(self, request_id: str) -> bytes:
        return await self._poll_result(request_id)

    async def _download_image(self, image_url: str) -> bytes:
        headers = {
            "api_token": self.settings.bria_api_key,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(image_url, headers=headers)

        if response.status_code >= 400:
            raise ProviderError(
                f"Failed to download Bria image: {response.status_code} {response.text[:300]}"
            )

        return response.content

    def _extract_request_id(self, data: dict[str, Any]) -> str | None:
        candidates = [
            data.get("request_id"),
            data.get("requestId"),
            data.get("id"),
            data.get("job_id"),
            data.get("data", {}).get("request_id"),
            data.get("data", {}).get("requestId"),
            data.get("data", {}).get("id"),
            data.get("data", {}).get("job_id"),
        ]

        for value in candidates:
            if isinstance(value, str) and value.strip():
                return value

        return None

    def _extract_image_url(self, data: dict[str, Any]) -> str | None:
        candidates = [
            data.get("result_url"),
            data.get("image_url"),
            data.get("url"),
            data.get("output_url"),
            data.get("data", {}).get("result_url"),
            data.get("data", {}).get("image_url"),
            data.get("data", {}).get("url"),
            data.get("data", {}).get("output_url"),
            data.get("result", {}).get("image_url"),
            data.get("result", {}).get("url"),
        ]

        for value in candidates:
            if isinstance(value, str) and value.startswith("http"):
                return value

        return None