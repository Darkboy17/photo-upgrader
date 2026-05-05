/**
 * Controls for AI output style.
 * This keeps provider/light settings separate from the upload dropzone.
 */

import { LIGHT_TYPE_OPTIONS, PROVIDER_OPTIONS } from "@/lib/constants";
import type { BriaLightType, EnhancementProvider } from "@/types/api";

interface EnhancementControlsProps {
    provider: EnhancementProvider;
    lightType: BriaLightType;
    disabled?: boolean;
    onProviderChange: (provider: EnhancementProvider) => void;
    onLightTypeChange: (lightType: BriaLightType) => void;
}

export function EnhancementControls({
    provider,
    lightType,
    disabled,
    onProviderChange,
    onLightTypeChange,
}: EnhancementControlsProps) {
    return (
        <div className="grid gap-4 rounded-[2rem] border border-white/10 bg-white/10 p-5 shadow-2xl shadow-fuchsia-950/20 backdrop-blur-xl md:grid-cols-2">
            <label className="space-y-2">
                <span className="text-xs font-black uppercase tracking-[0.25em] text-fuchsia-200">
                    AI Engine
                </span>

                <select
                    value={provider}
                    disabled={disabled}
                    onChange={(event) => onProviderChange(event.target.value as EnhancementProvider)}
                    className="w-full rounded-2xl border border-white/10 bg-black/50 px-4 py-3 text-sm font-bold text-white outline-none ring-fuchsia-400 transition focus:ring-2 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {PROVIDER_OPTIONS.map((item) => (
                        <option key={item} value={item}>
                            {item.replaceAll("_", " ").toUpperCase()}
                        </option>
                    ))}
                </select>
            </label>

            <label className="space-y-2">
                <span className="text-xs font-black uppercase tracking-[0.25em] text-cyan-200">
                    Lighting Mood
                </span>

                <select
                    value={lightType}
                    disabled={disabled}
                    onChange={(event) => onLightTypeChange(event.target.value as BriaLightType)}
                    className="w-full rounded-2xl border border-white/10 bg-black/50 px-4 py-3 text-sm font-bold text-white outline-none ring-cyan-400 transition focus:ring-2 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {LIGHT_TYPE_OPTIONS.map((item) => (
                        <option key={item} value={item}>
                            {item}
                        </option>
                    ))}
                </select>
            </label>
        </div>
    );
}