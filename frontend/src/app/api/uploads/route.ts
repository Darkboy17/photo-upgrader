/**
 * Next.js upload proxy route.
 * This prevents exposing the FastAPI base URL directly in UI logic and keeps deployment flexible.
 */

import { NextResponse } from "next/server";

export async function POST(request: Request) {
    const backendUrl = process.env.BACKEND_API_URL;

    if (!backendUrl) {
        return NextResponse.json(
            { detail: "BACKEND_API_URL is not configured." },
            { status: 500 }
        );
    }

    const formData = await request.formData();

    const response = await fetch(`${backendUrl}/uploads`, {
        method: "POST",
        body: formData,
    });

    const payload = await response.json().catch(() => null);

    return NextResponse.json(payload, {
        status: response.status,
    });
}