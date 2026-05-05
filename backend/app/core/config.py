from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Photo Upgrader API"
    app_env: str = "development"
    app_debug: bool = True

    backend_base_url: str = "http://localhost:8000"

    cors_origins: str = "http://localhost:3000"

    max_upload_mb: int = 12
    allowed_image_types: str = "image/jpeg,image/png,image/webp"

    storage_input_dir: str = "storage/inputs"
    storage_output_dir: str = "storage/outputs"

    default_provider: str = "huggingface"

    hf_api_token: str | None = None
    hf_model: str = "stabilityai/stable-diffusion-x4-upscaler"

    stability_api_key: str | None = None
    
    bria_api_key: str | None = None
    bria_light_type: str = "soft overcast daylight lighting"
    bria_light_direction: str = "front"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_origin_list(self) -> list[str]:

        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def allowed_types_list(self) -> list[str]:
        return [mime.strip() for mime in self.allowed_image_types.split(",") if mime.strip()]

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
