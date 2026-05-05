from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile

from app.core.config import get_settings
from app.models.job import EnhancementProvider, InternalJob, JobCreateResponse, JobStatus
from app.services.enhancement_pipeline import EnhancementPipeline
from app.services.image_storage import ImageStorage
from app.services.image_validator import ImageValidator
from app.models.job import BriaLightType

router = APIRouter(prefix="/uploads", tags=["Uploads"])

JOBS: dict[str, InternalJob] = {}


async def run_enhancement_job(job_id: str, light_type: str | None = None):
    job = JOBS[job_id]
    job.status = JobStatus.processing

    try:
        pipeline = EnhancementPipeline()

        output_path = await pipeline.enhance_image(
            input_path=job.input_path,
            output_path=job.output_path or "",
            provider=job.provider,
            light_type=light_type,
        )

        output_filename = Path(output_path).name
        storage = ImageStorage()

        job.status = JobStatus.completed
        job.output_path = output_path
        job.enhanced_url = storage.public_output_url(output_filename)

    except Exception as exc:
        job.status = JobStatus.failed
        job.error = str(exc)


@router.post("", response_model=JobCreateResponse)
async def upload_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    provider: EnhancementProvider | None = Form(default=None),
    light_type: BriaLightType | None = Form(default=None),
):
    settings = get_settings()
    validator = ImageValidator()
    storage = ImageStorage()

    data = await validator.validate_upload(file)

    extension = "jpg"
    if file.content_type == "image/png":
        extension = "png"
    elif file.content_type == "image/webp":
        extension = "webp"

    job_id, input_path = await storage.save_input(data, extension)
    input_filename = Path(input_path).name

    output_path = storage.output_path_for(job_id)

    selected_provider = provider or EnhancementProvider(
        settings.default_provider)

    print("DEFAULT_PROVIDER:", settings.default_provider)
    print("REQUEST_PROVIDER:", provider)
    print("SELECTED_PROVIDER:", selected_provider)

    job = InternalJob(
        job_id=job_id,
        status=JobStatus.queued,
        input_path=input_path,
        output_path=output_path,
        original_url=storage.public_input_url(input_filename),
        provider=selected_provider,
    )

    JOBS[job_id] = job

    background_tasks.add_task(
        run_enhancement_job, job_id, light_type.value if light_type else None)

    return JobCreateResponse(
        job_id=job_id,
        status=job.status,
        original_url=job.original_url or "",
    )
