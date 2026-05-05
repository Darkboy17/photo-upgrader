/**
 * Centralized frontend constants.
 * Keeping options here avoids scattering API-specific values across UI components.
 */

import type { BriaLightType, EnhancementProvider } from "@/types/api";

export const PROVIDER_OPTIONS: EnhancementProvider[] = ["bria_relight"];

export const LIGHT_TYPE_OPTIONS: BriaLightType[] = [
    "midday",
    "blue hour light",
    "low-angle sunlight",
    "sunrise light",
    "spotlight on subject",
    "overcast light",
    "soft overcast daylight lighting",
    "cloud-filtered lighting",
    "fog-diffused lighting",
    "moonlight lighting",
    "starlight nighttime",
    "soft bokeh lighting",
    "harsh studio lighting",
];

export const MAX_FILE_SIZE_MB = 12;

export const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];