from abc import ABC, abstractmethod


class ImageEnhancementProvider(ABC):
    @abstractmethod
    async def enhance(self, image_bytes: bytes) -> bytes:
        raise NotImplementedError
