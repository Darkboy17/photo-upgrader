/**
 * Next.js job polling proxy.
 * The frontend polls this route, which forwards the request to FastAPI.
 */

import { NextResponse } from "next/server";

interface RouteContext {
    params: Promise<{
        jobId: string;
    }>;
}

export async function GET(_request: Request, context: RouteContext) {
    const backendUrl = process.env.BACKEND_API_URL;

    if (!backendUrl) {
        return NextResponse.json(
            { detail: "BACKEND_API_URL is not configured." },
            { status: 500 }
        );
    }

    const { jobId } = await context.params;

    const response = await fetch(`${backendUrl}/jobs/${jobId}`, {
        method: "GET",
        cache: "no-store",
    });

    const payload = await response.json().catch(() => null);

    return NextResponse.json(payload, {
        status: response.status,
    });
}