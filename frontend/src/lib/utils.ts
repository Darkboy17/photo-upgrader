/**
 * Small UI utilities.
 * These helpers keep class composition and formatting clean inside components.
 */

import clsx, { type ClassValue } from "clsx";

export function cn(...classes: ClassValue[]) {
    return clsx(classes);
}

export function formatBytes(bytes: number) {
    if (bytes === 0) return "0 Bytes";

    const units = ["Bytes", "KB", "MB"];
    const index = Math.floor(Math.log(bytes) / Math.log(1024));

    return `${Number.parseFloat((bytes / 1024 ** index).toFixed(2))} ${units[index]}`;
}