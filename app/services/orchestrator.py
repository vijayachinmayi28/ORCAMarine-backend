from app.models import (
    AskResponse,
    LocationResult,
    Source,
)
from app.services.geocoding import geocode_location
from app.services.marine import get_marine
from app.services.mpa import check_mpa
from app.services.safety import assess_safety
from app.services.weather import get_weather


SOURCES = [
    Source(
        name="Open-Meteo Weather",
        url="https://open-meteo.com/en/docs",
    ),
    Source(
        name="Open-Meteo Marine",
        url="https://open-meteo.com/en/docs/marine-weather-api",
    ),
    Source(
        name="OpenStreetMap Nominatim",
        url="https://nominatim.openstreetmap.org/",
    ),
]


async def answer_question(
    location: str,
    question: str,
    request_id: str,
) -> AskResponse:
    errors: list[str] = []

    geo = await geocode_location(location)

    location_result = LocationResult(
        query=location,
        resolved_name=geo.resolved_name,
        latitude=geo.latitude,
        longitude=geo.longitude,
    )

    from app.models import WeatherData, MarineData, ProtectedArea

    if geo.latitude is None or geo.longitude is None:
        return AskResponse(
            request_id=request_id,
            location=location_result,
            answer=(
                "I could not resolve that location. In DEMO_MODE, try "
                "Mumbai Coast, Chennai Coast, Goa, or Bengaluru."
            ),
            safety=assess_safety(MarineData(status="UNAVAILABLE"), WeatherData(status="UNAVAILABLE")),
            weather=WeatherData(status="UNAVAILABLE"),
            marine=MarineData(status="UNAVAILABLE"),
            protected_area=ProtectedArea(status="NOT_CHECKED"),
            sources=SOURCES,
            demo_mode=True,
            generated_at="1970-01-01T00:00:00Z",
            errors=["Location could not be geocoded."],
        )

    marine = MarineData(status="UNAVAILABLE")
    weather = WeatherData(status="UNAVAILABLE")

    try:
        weather = await get_weather(geo.latitude, geo.longitude)
    except Exception as exc:
        errors.append(f"Weather service unavailable: {type(exc).__name__}")

    try:
        marine = await get_marine(geo.latitude, geo.longitude)
    except Exception as exc:
        errors.append(f"Marine service unavailable: {type(exc).__name__}")

    try:
        protected_area = check_mpa(geo.latitude, geo.longitude)
    except Exception as exc:
        errors.append(f"MPA service unavailable: {type(exc).__name__}")
        protected_area = ProtectedArea(status="MPA_DATA_UNAVAILABLE")

    safety = assess_safety(marine, weather)

    answer = (
        f"Assessment for {geo.resolved_name or location}: "
        f"{safety.verdict}. {safety.disclaimer}"
    )

    return AskResponse(
        request_id=request_id,
        location=location_result,
        answer=answer,
        safety=safety,
        weather=weather,
        marine=marine,
        protected_area=protected_area,
        distance_to_coast_km=None,
        distance_status="COASTLINE_DATA_NOT_CONFIGURED",
        sources=SOURCES,
        demo_mode=__import__("app.config", fromlist=["settings"]).settings.demo_mode,
        generated_at="1970-01-01T00:00:00Z",
        errors=errors,
    )
