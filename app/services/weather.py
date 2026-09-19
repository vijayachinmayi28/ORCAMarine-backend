from app.config import settings
from app.models import WeatherData
from app.utils.http import get_json


DEMO_WEATHER = WeatherData(
    temperature_c=29.0,
    wind_speed_kmh=18.0,
    wind_gusts_kmh=28.0,
    precipitation_probability=20.0,
    weather_code=2,
    status="DEMO",
)


async def get_weather(latitude: float, longitude: float) -> WeatherData:
    if settings.demo_mode:
        return DEMO_WEATHER.model_copy()

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation,weather_code",
        "hourly": "precipitation_probability",
        "timezone": "auto",
        "forecast_days": 1,
    }

    data = await get_json(
        settings.open_meteo_url,
        params=params,
        timeout=settings.http_timeout_seconds,
    )

    current = data.get("current", {})
    hourly = data.get("hourly", {})
    probabilities = hourly.get("precipitation_probability") or []

    return WeatherData(
        temperature_c=current.get("temperature_2m"),
        wind_speed_kmh=current.get("wind_speed_10m"),
        wind_gusts_kmh=current.get("wind_gusts_10m"),
        precipitation_probability=probabilities[0] if probabilities else None,
        weather_code=current.get("weather_code"),
        status="OK",
    )
