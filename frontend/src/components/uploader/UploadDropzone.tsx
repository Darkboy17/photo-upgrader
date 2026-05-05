"use client";

/**
 * Drag-and-drop image uploader.
 * Handles local file validation, preview creation, and upload submission.
 */

import { ChangeEvent, DragEvent, useEffect, useRef, useState } from "react";
import { ImagePlus, Sparkles, UploadCloud, X } from "lucide-react";

import { ACCEPTED_IMAGE_TYPES, MAX_FILE_SIZE_MB } from "@/lib/constants";
import { cn, formatBytes } from "@/lib/utils";
import type { BriaLightType, EnhancementProvider } from "@/types/api";

interface UploadDropzoneProps {
    disabled?: boolean;
    provider: EnhancementProvider;
    lightType: BriaLightType;
    onSubmit: (file: File) => void;
}

export function UploadDropzone({
    disabled,
    provider,
    lightType,
    onSubmit,
}: UploadDropzoneProps) {
    const inputRef = useRef<HTMLInputElement | null>(null);
    const [file, setFile] = useState<File | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    useEffect(() => {
        return () => {
            if (previewUrl) {
                URL.revokeObjectURL(previewUrl);
            }
        };
    }, [previewUrl]);

    function validateFile(nextFile: File) {
        if (!ACCEPTED_IMAGE_TYPES.includes(nextFile.type)) {
            return "Please upload a JPG, PNG, or WEBP image.";
        }

        if (nextFile.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
            return `File must be smaller than ${MAX_FILE_SIZE_MB}MB.`;
        }

        return null;
    }

    function handleFile(nextFile: File) {
        const validationError = validateFile(nextFile);

        if (validationError) {
            setError(validationError);
            setFile(null);

            if (previewUrl) {
                URL.revokeObjectURL(previewUrl);
            }

            setPreviewUrl(null);
            return;
        }

        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
        }

        const objectUrl = URL.createObjectURL(nextFile);

        setError(null);
        setFile(nextFile);
        setPreviewUrl(objectUrl);
    }

    function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
        const nextFile = event.target.files?.[0];

        if (nextFile) {
            handleFile(nextFile);
        }
    }

    function handleDrop(event: DragEvent<HTMLDivElement>) {
        event.preventDefault();
        setIsDragging(false);

        const nextFile = event.dataTransfer.files?.[0];

        if (nextFile) {
            handleFile(nextFile);
        }
    }

    return (
        <div className="rounded-[2.5rem] border border-white/10 bg-white/[0.08] p-4 shadow-2xl shadow-purple-950/30 backdrop-blur-2xl">
            <div
                onDragOver={(event) => {
                    event.preventDefault();
                    setIsDragging(true);
                }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
                className={cn(
                    "group relative flex min-h-[420px] cursor-pointer flex-col items-center justify-center overflow-hidden rounded-[2rem] border-2 border-dashed p-6 text-center transition",
                    isDragging
                        ? "border-fuchsia-300 bg-fuchsia-400/20"
                        : "border-white/15 bg-black/30 hover:border-cyan-300/70 hover:bg-white/10"
                )}
            >
                <input
                    ref={inputRef}
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    disabled={disabled}
                    onChange={handleInputChange}
                    className="hidden"
                />

                {previewUrl ? (
                    <div className="relative h-full w-full">
                        <button
                            type="button"
                            disabled={disabled}
                            onClick={(event) => {
                                event.stopPropagation();

                                if (previewUrl) {
                                    URL.revokeObjectURL(previewUrl);
                                }

                                setFile(null);
                                setPreviewUrl(null);
                            }}
                            className="absolute right-4 top-4 z-10 rounded-full bg-black/70 p-2 text-white shadow-lg backdrop-blur transition hover:scale-110"
                        >
                            <X size={18} />
                        </button>

                        <img
                            src={previewUrl}
                            alt="Selected upload preview"
                            className="mx-auto max-h-[360px] rounded-3xl object-contain shadow-2xl shadow-black/50"
                        />

                        <div className="mt-5 rounded-2xl bg-white/10 p-4 text-left">
                            <p className="font-black text-white">{file?.name}</p>
                            <p className="text-sm text-white/60">{file ? formatBytes(file.size) : null}</p>
                        </div>
                    </div>
                ) : (
                    <>
                        <div className="mb-6 rounded-[2rem] bg-gradient-to-br from-fuchsia-500 via-purple-500 to-cyan-400 p-5 shadow-2xl shadow-fuchsia-500/30 transition group-hover:scale-110">
                            <ImagePlus className="h-12 w-12 text-white" />
                        </div>

                        <h2 className="max-w-xl text-3xl font-black tracking-tight text-white md:text-5xl">
                            Drop the ugly product photo here.
                        </h2>

                        <p className="mt-4 max-w-lg text-base font-medium text-white/60">
                            Drag an Alibaba-style low-res image and turn it into a punchy studio-ready shot.
                        </p>

                        <div className="mt-8 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-5 py-3 text-sm font-black uppercase tracking-[0.2em] text-cyan-100">
                            <UploadCloud size={18} />
                            Browse Image
                        </div>
                    </>
                )}
            </div>

            {error ? (
                <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm font-bold text-red-100">
                    {error}
                </p>
            ) : null}

            <button
                type="button"
                disabled={!file || disabled}
                onClick={() => file && onSubmit(file)}
                className="mt-5 flex w-full items-center justify-center gap-3 rounded-3xl bg-gradient-to-r from-fuchsia-500 via-purple-500 to-cyan-400 px-6 py-4 text-base font-black uppercase tracking-[0.25em] text-white shadow-2xl shadow-fuchsia-700/30 transition hover:-translate-y-1 hover:shadow-cyan-500/20 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0"
            >
                <Sparkles size={20} />
                {disabled ? "Cooking Pixels..." : "Upgrade Photo"}
            </button>

            <p className="mt-4 text-center text-xs font-medium text-white/40">
                Provider: {provider} · Lighting: {lightType}
            </p>
        </div>
    );
}