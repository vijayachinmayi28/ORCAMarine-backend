from app.models import MarineData, SafetyAssessment, WeatherData


def assess_safety(
    marine: MarineData,
    weather: WeatherData,
) -> SafetyAssessment:
    reasons: list[str] = []
    risk_points = 0
    data_available = False

    wave = marine.wave_height_m
    wind = weather.wind_speed_kmh
    gust = weather.wind_gusts_kmh

    if wave is not None:
        data_available = True
        if wave >= 2.5:
            risk_points += 60
            reasons.append("Very high wave height in the available forecast.")
        elif wave >= 1.5:
            risk_points += 35
            reasons.append("High wave height in the available forecast.")
        elif wave >= 0.8:
            risk_points += 15
            reasons.append("Moderate wave height in the available forecast.")
        else:
            reasons.append("Low wave height in the available forecast.")

    if wind is not None:
        data_available = True
        if wind > 35:
            risk_points += 40
            reasons.append("High sustained wind speed.")
        elif wind >= 20:
            risk_points += 20
            reasons.append("Moderate sustained wind speed.")
        else:
            reasons.append("Low sustained wind speed.")

    if gust is not None and gust > 40:
        risk_points += 20
        reasons.append("Strong wind gusts are present.")

    if not data_available:
        return SafetyAssessment(
            verdict="UNKNOWN",
            score=None,
            reasons=["Insufficient marine/weather data for an assessment."],
        )

    score = min(100, risk_points)

    if score >= 60:
        verdict = "HIGH_RISK"
    elif score >= 25:
        verdict = "CAUTION"
    else:
        verdict = "SAFE"

    return SafetyAssessment(
        verdict=verdict,
        score=score,
        reasons=reasons,
    )
