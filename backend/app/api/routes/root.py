from fastapi import APIRouter

router = APIRouter(tags=["Root"])


@router.get("/", summary="Root endpoint")
def root():
    return {
        "message": "Welcome to the Photo Upgrader API",
    }