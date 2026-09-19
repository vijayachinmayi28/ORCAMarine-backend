from dataclasses import dataclass

from app.config import settings
from app.utils.http import get_json


@dataclass
class GeocodedLocation:
    query: str
    resolved_name: str | None
    latitude: float | None
    longitude: float | None
    status: str


DEMO_LOCATIONS = {
    "mumbai coast": ("Mumbai, Maharashtra, India", 19.0760, 72.8777),
    "mumbai": ("Mumbai, Maharashtra, India", 19.0760, 72.8777),
    "chennai coast": ("Chennai, Tamil Nadu, India", 13.0827, 80.2707),
    "chennai": ("Chennai, Tamil Nadu, India", 13.0827, 80.2707),
    "goa": ("Goa, India", 15.2993, 74.1240),
    "bengaluru": ("Bengaluru, Karnataka, India", 12.9716, 77.5946),
}


async def geocode_location(location: str) -> GeocodedLocation:
    key = location.strip().lower()

    if settings.demo_mode and key in DEMO_LOCATIONS:
        name, lat, lon = DEMO_LOCATIONS[key]
        return GeocodedLocation(location, name, lat, lon, "DEMO")

    if settings.demo_mode:
        return GeocodedLocation(
            location, location, None, None, "DEMO_LOCATION_NOT_CONFIGURED"
        )

    params = {"q": location, "format": "jsonv2", "limit": 1}
    headers = {"User-Agent": settings.user_agent}
    data = await get_json(
        settings.nominatim_url,
        params=params,
        headers=headers,
        timeout=settings.http_timeout_seconds,
    )

    if not data:
        return GeocodedLocation(location, None, None, None, "NOT_FOUND")

    item = data[0]
    return GeocodedLocation(
        query=location,
        resolved_name=item.get("display_name"),
        latitude=float(item["lat"]),
        longitude=float(item["lon"]),
        status="OK",
    )
