from pathlib import Path

from app.core.errors import ProviderError
from app.models.job import EnhancementProvider
from app.services.image_preprocessor import ImagePreprocessor
from app.services.providers.huggingface_provider import HuggingFaceProvider
from app.services.providers.stability_provider import StabilityProvider

from app.services.providers.bria_relight_provider import BriaRelightProvider


class EnhancementPipeline:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()

    async def enhance_image(
        self,
        input_path: str,
        output_path: str,
        provider: EnhancementProvider,
        light_type: str | None = None,
    ) -> str:
        prepared_bytes = self.preprocessor.prepare_for_ai(input_path)

        ai_provider = self._get_provider(provider, light_type)
        enhanced_bytes = await ai_provider.enhance(prepared_bytes)

        self.preprocessor.postprocess_output(enhanced_bytes, output_path)

        if not Path(output_path).exists():
            raise ProviderError("Output image was not created.")

        return output_path

    def _get_provider(self, provider: EnhancementProvider, light_type: str | None = None):
        if provider == EnhancementProvider.huggingface:
            return HuggingFaceProvider()

        if provider == EnhancementProvider.stability:
            return StabilityProvider()
        
        if provider == EnhancementProvider.bria_relight:
            return BriaRelightProvider(light_type=light_type)

        raise ProviderError(f"Unsupported provider: {provider}")
