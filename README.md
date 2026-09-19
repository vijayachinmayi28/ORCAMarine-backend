# ORCAMarine Backend

AI Marine Safety Assistant backend for the SIH project.

## What it does

`POST /ask` accepts a location and question, resolves the location, gathers weather/marine information, checks a local MPA GeoJSON file, and produces a deterministic informational safety assessment.

The backend has two modes:

- `DEMO_MODE=true`: deterministic data, no external API dependency required.
- `DEMO_MODE=false`: calls Nominatim and Open-Meteo.

## Run locally on Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## Test

```powershell
python -m pytest
```

## Example

```json
{
  "location": "Mumbai Coast",
  "question": "Is it safe to swim today?"
}
```

## MPA data

`data/mpa.geojson` starts as an empty FeatureCollection. Replace it with an appropriate official MPA dataset before claiming real protected-area coverage. The code supports GeoJSON FeatureCollection/Feature with Polygon/MultiPolygon geometries.

## Safety disclaimer

The safety engine is an informational hackathon demo. It is not official maritime safety advice and its thresholds must not be represented as official safety standards.

## Future agentic AI

A future agent can orchestrate the service functions:

- `geocode_location`
- `get_weather`
- `get_marine`
- `check_mpa`
- `assess_safety`

The FastAPI route does not need to contain the agent logic.
