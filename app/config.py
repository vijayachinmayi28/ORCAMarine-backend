from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ORCAMarine API"
    demo_mode: bool = False
    http_timeout_seconds: float = 8.0

    nominatim_url: str = "https://nominatim.openstreetmap.org/search"
    open_meteo_url: str = "https://api.open-meteo.com/v1/forecast"
    open_meteo_marine_url: str = "https://marine-api.open-meteo.com/v1/marine"

    mpa_file: str = "data/mpa.geojson"
    allowed_origins: str = "*"
    user_agent: str = "ORCAMarine-Hackathon/1.0"

    max_location_length: int = 200
    max_question_length: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        if self.allowed_origins.strip() == "*":
            return ["*"]
        return [x.strip() for x in self.allowed_origins.split(",") if x.strip()]

    @property
    def mpa_path(self) -> Path:
        return Path(self.mpa_file)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
