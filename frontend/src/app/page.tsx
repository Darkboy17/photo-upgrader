"use client";

/**
 * Main application screen.
 * Coordinates upload, polling, and result rendering while keeping UI pieces separated.
 */

import { useEffect, useState } from "react";

import { AppShell } from "@/components/layout/AppShell";
import { EnhancementControls } from "@/components/uploader/EnhancementControls";
import { UploadDropzone } from "@/components/uploader/UploadDropzone";
import { ResultPanel } from "@/components/viewer/ResultPanel";
import { getJob, uploadImage } from "@/lib/api";
import type {
  BriaLightType,
  EnhancementProvider,
  JobResultResponse,
  UploadResponse,
} from "@/types/api";

export default function Home() {
  const [provider, setProvider] = useState<EnhancementProvider>("bria_relight");
  const [lightType, setLightType] = useState<BriaLightType>("soft overcast daylight lighting");

  const [upload, setUpload] = useState<UploadResponse | null>(null);
  const [job, setJob] = useState<JobResultResponse | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  async function handleSubmit(file: File) {
    setIsUploading(true);
    setUpload(null);
    setJob(null);

    try {
      const response = await uploadImage({
        file,
        provider,
        lightType,
      });

      setUpload(response);
      setJob({
        job_id: response.job_id,
        status: response.status,
        original_url: response.original_url,
        enhanced_url: null,
        error: null,
      });
    } catch (error) {
      setUpload(null);

      setJob({
        job_id: "local-error",
        status: "failed",
        original_url: null,
        enhanced_url: null,
        error: error instanceof Error ? error.message : "Upload failed.",
      });
    } finally {
      setIsUploading(false);
    }
  }

  useEffect(() => {
    if (!upload?.job_id) return;

    const intervalId = window.setInterval(async () => {
      try {
        const result = await getJob(upload.job_id);
        setJob(result);

        if (result.status === "completed" || result.status === "failed") {
          window.clearInterval(intervalId);
        }
      } catch (error) {
        setJob({
          job_id: upload.job_id,
          status: "failed",
          original_url: upload.original_url,
          enhanced_url: null,
          error: error instanceof Error ? error.message : "Polling failed.",
        });

        window.clearInterval(intervalId);
      }
    }, 2000);

    return () => window.clearInterval(intervalId);
  }, [upload]);

  const isBusy = isUploading || job?.status === "queued" || job?.status === "processing";

  return (
    <AppShell>
      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="space-y-6">
          <EnhancementControls
            provider={provider}
            lightType={lightType}
            disabled={isBusy}
            onProviderChange={setProvider}
            onLightTypeChange={setLightType}
          />

          <UploadDropzone
            disabled={isBusy}
            provider={provider}
            lightType={lightType}
            onSubmit={handleSubmit}
          />
        </div>

        <ResultPanel job={job} />
      </section>
    </AppShell>
  );
}