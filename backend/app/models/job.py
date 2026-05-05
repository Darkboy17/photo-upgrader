from enum import Enum
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class EnhancementProvider(str, Enum):
    huggingface = "huggingface"
    stability = "stability"
    bria_relight = "bria_relight"


class JobCreateResponse(BaseModel):
    job_id: str
    status: JobStatus
    original_url: str


class JobResultResponse(BaseModel):
    job_id: str
    status: JobStatus
    original_url: str | None = None
    enhanced_url: str | None = None
    error: str | None = None


class InternalJob(BaseModel):
    job_id: str
    status: JobStatus = JobStatus.queued
    input_path: str
    output_path: str | None = None
    original_url: str | None = None
    enhanced_url: str | None = None
    error: str | None = None
    provider: EnhancementProvider = Field(
        default=EnhancementProvider.huggingface)


class BriaLightType(str, Enum):
    midday = "midday"
    blue_hour_light = "blue hour light"
    low_angle_sunlight = "low-angle sunlight"
    sunrise_light = "sunrise light"
    spotlight_on_subject = "spotlight on subject"
    overcast_light = "overcast light"
    soft_overcast_daylight_lighting = "soft overcast daylight lighting"
    cloud_filtered_lighting = "cloud-filtered lighting"
    fog_diffused_lighting = "fog-diffused lighting"
    side_lighting = "side lighting"
    moonlight_lighting = "moonlight lighting"
    starlight_nighttime = "starlight nighttime"
    soft_bokeh_lighting = "soft bokeh lighting"
    harsh_studio_lighting = "harsh studio lighting"