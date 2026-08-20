from app.models.analysis import (
    AnalysisReport,
    AnalysisScore,
)


def generate_report(
    symbol: str,
    price: float,
    score: AnalysisScore,
):
    strengths = []
    risks = []
    observations = []

    components = [
        score.trend,
        score.momentum,
        score.volatility,
        score.structure,
    ]

    for component in components:

        if component.score >= 70:
            strengths.append(
                f"{component.label}: "
                f"{component.explanation}"
            )

        if component.score <= 40:
            risks.append(
                f"{component.label}: "
                f"{component.explanation}"
            )

        observations.append(
            component.explanation
        )

    if score.overall >= 75:

        bias = "BULLISH"
        confidence = "HIGH"

        summary = (
            f"{symbol} currently shows a "
            "strongly positive technical profile. "
            "Multiple analytical components are "
            "aligned in the same direction."
        )

    elif score.overall >= 60:

        bias = "BULLISH"
        confidence = "MODERATE"

        summary = (
            f"{symbol} currently shows a "
            "generally positive technical profile, "
            "although some components may not be "
            "fully aligned."
        )

    elif score.overall >= 45:

        bias = "NEUTRAL"
        confidence = "LOW"

        summary = (
            f"{symbol} currently shows a mixed "
            "technical profile. The available "
            "signals do not strongly favor "
            "either direction."
        )

    elif score.overall >= 30:

        bias = "BEARISH"
        confidence = "MODERATE"

        summary = (
            f"{symbol} currently shows a generally "
            "weak technical profile."
        )

    else:

        bias = "BEARISH"
        confidence = "HIGH"

        summary = (
            f"{symbol} currently shows a strongly "
            "negative technical profile."
        )

    return AnalysisReport(
        symbol=symbol,
        price=price,

        market_bias=bias,
        confidence=confidence,

        score=score,

        summary=summary,

        strengths=strengths,
        risks=risks,
        observations=observations,
  )
