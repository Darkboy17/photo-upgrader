"use client";

/**
 * Before/after result viewer.
 * Includes a hover-only fullscreen button for inspecting the enhanced image.
 */

import { useState } from "react";
import { ArrowLeftRight, Maximize2, X } from "lucide-react";

interface BeforeAfterViewerProps {
    beforeUrl: string;
    afterUrl: string;
}

export function BeforeAfterViewer({ beforeUrl, afterUrl }: BeforeAfterViewerProps) {
    const [view, setView] = useState<"before" | "after">("after");
    const [isFullscreenOpen, setIsFullscreenOpen] = useState(false);

    const activeUrl = view === "before" ? beforeUrl : afterUrl;

    return (
        <>
            <div className="group relative overflow-hidden rounded-[2.5rem] border border-white/10 bg-black/50 p-4 shadow-2xl shadow-cyan-950/30">
                <div className="absolute right-6 top-6 z-10 flex rounded-full border border-white/10 bg-black/70 p-1 backdrop-blur-xl">
                    <button
                        type="button"
                        onClick={() => setView("before")}
                        className={`rounded-full px-4 py-2 text-xs font-black uppercase tracking-[0.2em] transition ${view === "before" ? "bg-white text-black" : "text-white/60 hover:text-white"
                            }`}
                    >
                        Before
                    </button>

                    <button
                        type="button"
                        onClick={() => setView("after")}
                        className={`rounded-full px-4 py-2 text-xs font-black uppercase tracking-[0.2em] transition ${view === "after" ? "bg-cyan-300 text-black" : "text-white/60 hover:text-white"
                            }`}
                    >
                        After
                    </button>
                </div>

                <button
                    type="button"
                    onClick={() => setIsFullscreenOpen(true)}
                    className="absolute bottom-8 right-8 z-10 flex translate-y-3 items-center gap-2 rounded-full border border-white/10 bg-white px-5 py-3 text-xs font-black uppercase tracking-[0.2em] text-black opacity-0 shadow-2xl transition duration-300 hover:scale-105 group-hover:translate-y-0 group-hover:opacity-100"
                >
                    <Maximize2 size={16} />
                    View Fullscreen
                </button>

                <div className="flex min-h-[460px] items-center justify-center rounded-[2rem] bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.16),transparent_35%),radial-gradient(circle_at_bottom_left,rgba(217,70,239,0.18),transparent_35%)] p-6">
                    <img
                        src={activeUrl}
                        alt={`${view} product result`}
                        className="max-h-[520px] rounded-3xl object-contain shadow-2xl shadow-black/60"
                    />
                </div>

                <div className="mt-4 flex items-center justify-center gap-2 text-sm font-bold text-white/60">
                    <ArrowLeftRight size={16} />
                    Toggle top-right to compare result quality.
                </div>
            </div>

            {isFullscreenOpen ? (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-6 backdrop-blur-xl">
                    <button
                        type="button"
                        onClick={() => setIsFullscreenOpen(false)}
                        className="absolute right-6 top-6 rounded-full bg-white p-3 text-black shadow-2xl transition hover:scale-110"
                    >
                        <X size={22} />
                    </button>

                    <img
                        src={afterUrl}
                        alt="Fullscreen relighted result"
                        className="max-h-[92vh] max-w-[92vw] rounded-3xl object-contain shadow-2xl shadow-black"
                    />
                </div>
            ) : null}
        </>
    );
}