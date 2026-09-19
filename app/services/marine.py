from app.config import settings
from app.models import MarineData
from app.utils.http import get_json


DEMO_MARINE = MarineData(
    wave_height_m=1.2,
    wave_direction_deg=245.0,
    wave_period_s=7.4,
    wave_peak_period_s=8.0,
    sea_surface_temperature_c=28.1,
    status="DEMO",
)


async def get_marine(latitude: float, longitude: float) -> MarineData:
    if settings.demo_mode:
        return DEMO_MARINE.model_copy()

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "wave_height,wave_direction,wave_period,"
            "wave_peak_period,sea_surface_temperature"
        ),
        "hourly": (
            "wave_height,wave_direction,wave_period,"
            "wave_peak_period,sea_surface_temperature"
        ),
        "timezone": "auto",
        "forecast_days": 1,
    }

    data = await get_json(
        settings.open_meteo_marine_url,
        params=params,
        timeout=settings.http_timeout_seconds,
    )

    current = data.get("current", {})

    return MarineData(
        wave_height_m=current.get("wave_height"),
        wave_direction_deg=current.get("wave_direction"),
        wave_period_s=current.get("wave_period"),
        wave_peak_period_s=current.get("wave_peak_period"),
        sea_surface_temperature_c=current.get("sea_surface_temperature"),
        status="OK",
    )
