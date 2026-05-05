/**
 * Visual shell for the landing app.
 * Keeps the page layout consistent and makes the UI feel like a polished SaaS product.
 */

import { ReactNode } from "react";
import { Camera, Zap } from "lucide-react";

interface AppShellProps {
    children: ReactNode;
}


export function AppShell({ children }: AppShellProps) {
    return (
        <main className="min-h-screen overflow-hidden bg-[#070711] text-white">
            <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_20%_10%,rgba(236,72,153,0.25),transparent_28%),radial-gradient(circle_at_80%_20%,rgba(34,211,238,0.22),transparent_30%),radial-gradient(circle_at_50%_90%,rgba(168,85,247,0.22),transparent_35%)]" />

            <div className="relative mx-auto flex w-full max-w-7xl flex-col gap-10 px-5 py-8 md:px-8 md:py-12">
                <header className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
                    <div>
                        <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-4 py-2 text-xs font-black uppercase tracking-[0.25em] text-cyan-100 backdrop-blur">
                            <Zap size={14} />
                            AI Product Glow-Up
                        </div>

                        <h1 className="mt-5 max-w-4xl text-5xl font-black tracking-[-0.06em] md:text-7xl">
                            Turn rough product shots into{" "}
                            <span className="bg-gradient-to-r from-fuchsia-300 via-purple-300 to-cyan-200 bg-clip-text text-transparent">
                                studio bangers.
                            </span>
                        </h1>

                        <p className="mt-5 max-w-2xl text-lg font-medium leading-8 text-white/60">
                            Drop in a low-res marketplace photo, pick the lighting, and generate a sharper, cleaner, sassier product visual.
                        </p>
                    </div>

                    <div className="hidden rounded-[2rem] border border-white/10 bg-white/10 p-5 shadow-2xl shadow-cyan-950/30 backdrop-blur-xl lg:block">
                        <Camera className="h-10 w-10 text-cyan-200" />
                        <p className="mt-4 max-w-[220px] text-sm font-bold text-white/70">
                            For best results, use clear product images with simple backgrounds. The AI will attempt to enhance the lighting and details, but it may not work perfectly on every photo.
                        </p>
                    </div>
                </header>

                {children}
            </div>
        </main>
    );
}