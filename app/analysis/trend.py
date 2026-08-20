from app.models.market import IndicatorSnapshot


def analyze_trend(
    price: float,
    indicators: IndicatorSnapshot,
):
    score = 50.0
    observations = []

    ema20 = indicators.ema_20
    ema50 = indicators.ema_50
    ema200 = indicators.ema_200

    if ema20 is not None:

        if price > ema20:
            score += 10
            observations.append(
                "Price is above EMA 20."
            )
        else:
            score -= 10
            observations.append(
                "Price is below EMA 20."
            )

    if ema50 is not None:

        if price > ema50:
            score += 10
            observations.append(
                "Price is above EMA 50."
            )
        else:
            score -= 10
            observations.append(
                "Price is below EMA 50."
            )

    if ema200 is not None:

        if price > ema200:
            score += 15
            observations.append(
                "Price is above EMA 200."
            )
        else:
            score -= 15
            observations.append(
                "Price is below EMA 200."
            )

    if (
        ema20 is not None
        and ema50 is not None
    ):

        if ema20 > ema50:
            score += 10
            observations.append(
                "EMA 20 is above EMA 50."
            )
        else:
            score -= 10
            observations.append(
                "EMA 20 is below EMA 50."
            )

    if (
        ema50 is not None
        and ema200 is not None
    ):

        if ema50 > ema200:
            score += 15
            observations.append(
                "EMA 50 is above EMA 200."
            )
        else:
            score -= 15
            observations.append(
                "EMA 50 is below EMA 200."
            )

    score = max(0, min(100, score))

    if score >= 70:
        label = "BULLISH"
    elif score >= 55:
        label = "SLIGHTLY BULLISH"
    elif score <= 30:
        label = "BEARISH"
    elif score <= 45:
        label = "SLIGHTLY BEARISH"
    else:
        label = "NEUTRAL"

    return score, label, observations
