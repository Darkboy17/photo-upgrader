from fastapi import APIRouter

from app.api.routes.uploads import JOBS
from app.core.errors import JobNotFoundError
from app.models.job import JobResultResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/{job_id}", response_model=JobResultResponse)
def get_job(job_id: str):
    job = JOBS.get(job_id)

    if not job:
        raise JobNotFoundError()

    return JobResultResponse(
        job_id=job.job_id,
        status=job.status,
        original_url=job.original_url,
        enhanced_url=job.enhanced_url,
        error=job.error,
    )
