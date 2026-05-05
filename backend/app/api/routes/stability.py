from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter

from app.services.image_storage import ImageStorage
from app.services.image_preprocessor import ImagePreprocessor
from app.services.providers.stability_relight_provider import StabilityRelightProvider

router = APIRouter(prefix="/stability", tags=["Stability"])


@router.get("/results/{generation_id}")
async def poll_stability_result(generation_id: str):
    provider = StabilityRelightProvider()
    image_bytes = await provider._poll_result(generation_id)

    storage = ImageStorage()
    preprocessor = ImagePreprocessor()

    output_id = str(uuid4())
    output_path = storage.output_path_for(output_id)

    preprocessor.postprocess_output(image_bytes, output_path)

    output_filename = Path(output_path).name

    return {
        "status": "completed",
        "generation_id": generation_id,
        "enhanced_url": storage.public_output_url(output_filename),
    }
