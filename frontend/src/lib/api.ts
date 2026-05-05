/**
 * Browser-side API client.
 * The browser talks to Next.js route handlers, and route handlers proxy to FastAPI.
 */

import type {
    BriaLightType,
    EnhancementProvider,
    JobResultResponse,
    UploadResponse,
} from "@/types/api";

export async function uploadImage(params: {
    file: File;
    provider: EnhancementProvider;
    lightType: BriaLightType;
}): Promise<UploadResponse> {
    const formData = new FormData();

    formData.append("file", params.file);
    formData.append("provider", params.provider);
    formData.append("light_type", params.lightType);

    const response = await fetch("/api/uploads", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail || "Upload failed.");
    }

    return response.json();
}

export async function getJob(jobId: string): Promise<JobResultResponse> {
    const response = await fetch(`/api/jobs/${jobId}`, {
        method: "GET",
        cache: "no-store",
    });

    if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail || "Failed to fetch job.");
    }

    return response.json();
}