/**
 * Result state renderer.
 * Handles queued/processing/failed/completed states separately to keep the page component clean.
 */

import { AlertTriangle, Loader2, WandSparkles } from "lucide-react";

import { BeforeAfterViewer } from "@/components/viewer/BeforeAfterViewer";
import type { JobResultResponse } from "@/types/api";

interface ResultPanelProps {
    job: JobResultResponse | null;
}

export function ResultPanel({ job }: ResultPanelProps) {
    if (!job) {
        return (
            <div className="flex min-h-[420px] flex-col items-center justify-center rounded-[2.5rem] border border-white/10 bg-white/[0.06] p-8 text-center backdrop-blur-xl">
                <div className="rounded-[2rem] bg-white/10 p-5">
                    <WandSparkles className="h-12 w-12 text-fuchsia-300" />
                </div>

                <h3 className="mt-6 text-3xl font-black text-white">Your glow-up appears here.</h3>
                <p className="mt-3 max-w-md text-white/55">
                    Upload a product image, choose the lighting mood, and watch the before/after studio result land here.
                </p>
            </div>
        );
    }

    if (job.status === "queued" || job.status === "processing") {
        return (
            <div className="flex min-h-[420px] flex-col items-center justify-center rounded-[2.5rem] border border-white/10 bg-white/[0.06] p-8 text-center backdrop-blur-xl">
                <Loader2 className="h-12 w-12 animate-spin text-cyan-300" />

                <h3 className="mt-6 text-3xl font-black text-white">
                    Pixel kitchen is heating up.
                </h3>

                <p className="mt-3 max-w-md text-white/55">
                    Your image is being processed by the backend pipeline. This can take a few seconds depending on the provider.
                </p>
            </div>
        );
    }

    if (job.status === "failed") {
        return (
            <div className="flex min-h-[420px] flex-col items-center justify-center rounded-[2.5rem] border border-red-400/20 bg-red-500/10 p-8 text-center backdrop-blur-xl">
                <AlertTriangle className="h-12 w-12 text-red-200" />

                <h3 className="mt-6 text-3xl font-black text-white">The render crashed.</h3>

                <p className="mt-3 max-w-lg text-red-100/80">{job.error || "Unknown error."}</p>
            </div>
        );
    }

    if (job.original_url && job.enhanced_url) {
        return <BeforeAfterViewer beforeUrl={job.original_url} afterUrl={job.enhanced_url} />;
    }

    return null;
}