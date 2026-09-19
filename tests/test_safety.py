from app.models import MarineData, WeatherData
from app.services.safety import assess_safety


def test_low_risk():
    result = assess_safety(
        MarineData(wave_height_m=0.4),
        WeatherData(wind_speed_kmh=10),
    )
    assert result.verdict == "SAFE"


def test_high_wave():
    result = assess_safety(
        MarineData(wave_height_m=3.0),
        WeatherData(wind_speed_kmh=10),
    )
    assert result.verdict == "HIGH_RISK"
