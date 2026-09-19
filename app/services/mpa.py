import json
from pathlib import Path

from shapely.geometry import Point, shape

from app.config import settings
from app.models import ProtectedArea


def _load_features(path: Path):
    with path.open("r", encoding="utf-8") as f:
        geojson = json.load(f)

    if geojson.get("type") == "FeatureCollection":
        return geojson.get("features", [])
    if geojson.get("type") == "Feature":
        return [geojson]
    return []


def check_mpa(latitude: float, longitude: float) -> ProtectedArea:
    path = settings.mpa_path

    if not path.exists():
        return ProtectedArea(
            inside_mpa=None,
            status="MPA_DATA_UNAVAILABLE",
        )

    try:
        features = _load_features(path)
        point = Point(longitude, latitude)

        for feature in features:
            geometry = feature.get("geometry")
            if not geometry:
                continue

            geom = shape(geometry)
            if geom.contains(point) or geom.touches(point):
                props = feature.get("properties") or {}
                return ProtectedArea(
                    inside_mpa=True,
                    name=props.get("name") or props.get("NAME"),
                    id=str(props.get("id") or props.get("WDPAID"))
                    if (props.get("id") or props.get("WDPAID")) is not None
                    else None,
                    status="OK",
                )

        return ProtectedArea(
            inside_mpa=False,
            status="OK",
        )
    except Exception:
        return ProtectedArea(
            inside_mpa=None,
            status="MPA_DATA_INVALID",
        )
