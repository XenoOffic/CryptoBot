from app.models.market import IndicatorSnapshot


def analyze_volatility(
    price: float,
    indicators: IndicatorSnapshot,
):
    observations = []

    atr = indicators.atr

    if atr is None or price <= 0:
        return 50.0, "UNKNOWN", observations

    atr_percentage = (
        atr / price
    ) * 100

    observations.append(
        f"ATR is approximately "
        f"{atr_percentage:.2f}% of price."
    )

    if atr_percentage < 1:
        score = 80
        label = "LOW"

    elif atr_percentage < 3:
        score = 65
        label = "MODERATE"

    elif atr_percentage < 6:
        score = 45
        label = "HIGH"

    else:
        score = 25
        label = "EXTREME"

    return score, label, observations
