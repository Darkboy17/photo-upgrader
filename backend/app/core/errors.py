from fastapi import HTTPException, status


class AppError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class BadImageError(AppError):
    def __init__(self, detail: str = "Invalid image file."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class ProviderError(AppError):
    def __init__(self, detail: str = "AI provider failed."):
        super().__init__(status.HTTP_502_BAD_GATEWAY, detail)


class JobNotFoundError(AppError):
    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND, "Job not found.")
