from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    location: str = Field(..., min_length=1, max_length=200)
    question: str = Field(..., min_length=1, max_length=1000)

    @field_validator("location", "question")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value


class LocationResult(BaseModel):
    query: str
    resolved_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class WeatherData(BaseModel):
    temperature_c: float | None = None
    wind_speed_kmh: float | None = None
    wind_gusts_kmh: float | None = None
    precipitation_probability: float | None = None
    weather_code: int | None = None
    status: str = "OK"


class MarineData(BaseModel):
    wave_height_m: float | None = None
    wave_direction_deg: float | None = None
    wave_period_s: float | None = None
    wave_peak_period_s: float | None = None
    sea_surface_temperature_c: float | None = None
    status: str = "OK"


class ProtectedArea(BaseModel):
    inside_mpa: bool | None = None
    name: str | None = None
    id: str | None = None
    status: str = "OK"
    source: str = "local GeoJSON"


class SafetyAssessment(BaseModel):
    verdict: str
    score: int | None = None
    reasons: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "This is an informational demo assessment, not official maritime safety advice."
    )


class Source(BaseModel):
    name: str
    url: str


class AskResponse(BaseModel):
    request_id: str
    location: LocationResult
    answer: str
    safety: SafetyAssessment
    weather: WeatherData
    marine: MarineData
    protected_area: ProtectedArea
    distance_to_coast_km: float | None = None
    distance_status: str = "COASTLINE_DATA_NOT_CONFIGURED"
    sources: list[Source] = Field(default_factory=list)
    demo_mode: bool
    generated_at: datetime
    errors: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str
    demo_mode: bool
