from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import root, health, jobs, uploads, stability
from app.core.config import get_settings


def create_app() -> FastAPI:
    
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Path(settings.storage_input_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.storage_output_dir).mkdir(parents=True, exist_ok=True)

    app.mount(
        "/static/inputs",
        StaticFiles(directory=settings.storage_input_dir),
        name="input-images",
    )

    app.mount(
        "/static/outputs",
        StaticFiles(directory=settings.storage_output_dir),
        name="output-images",
    )

    app.include_router(root.router)
    app.include_router(health.router)
    app.include_router(uploads.router)
    app.include_router(jobs.router)
    app.include_router(stability.router)

    return app


app = create_app()
