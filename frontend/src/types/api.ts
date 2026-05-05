/**
 * Shared API types for the frontend.
 * These mirror the FastAPI response shapes so UI code stays type-safe.
 */

export type JobStatus = "queued" | "processing" | "completed" | "failed";

export type EnhancementProvider =
    | "huggingface"
    | "stability"
    | "stability_studio"
    | "stability_relight"
    | "claid"
    | "bria_relight"
    | "local_diffusers";

export type BriaLightType =
    | "midday"
    | "blue hour light"
    | "low-angle sunlight"
    | "sunrise light"
    | "spotlight on subject"
    | "overcast light"
    | "soft overcast daylight lighting"
    | "cloud-filtered lighting"
    | "fog-diffused lighting"
    | "side lighting"
    | "moonlight lighting"
    | "starlight nighttime"
    | "soft bokeh lighting"
    | "harsh studio lighting";

export interface UploadResponse {
    job_id: string;
    status: JobStatus;
    original_url: string;
}

export interface JobResultResponse {
    job_id: string;
    status: JobStatus;
    original_url: string | null;
    enhanced_url: string | null;
    error: string | null;
}