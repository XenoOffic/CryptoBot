from app.models.market import IndicatorSnapshot


def analyze_momentum(
    indicators: IndicatorSnapshot,
):
    score = 50.0
    observations = []

    rsi = indicators.rsi

    if rsi is not None:

        if 50 <= rsi <= 65:

            score += 15

            observations.append(
                f"RSI is {rsi:.1f}, "
                "showing positive momentum "
                "without extreme conditions."
            )

        elif rsi > 70:

            score += 5

            observations.append(
                f"RSI is {rsi:.1f}, "
                "indicating strong but potentially "
                "overextended momentum."
            )

        elif rsi < 30:

            score += 5

            observations.append(
                f"RSI is {rsi:.1f}, "
                "indicating oversold conditions."
            )

        elif rsi < 45:

            score -= 15

            observations.append(
                f"RSI is {rsi:.1f}, "
                "indicating weak momentum."
            )

        else:

            score += 5

            observations.append(
                f"RSI is {rsi:.1f}, "
                "indicating relatively neutral momentum."
            )

    macd = indicators.macd
    signal = indicators.macd_signal

    if (
        macd is not None
        and signal is not None
    ):

        if macd > signal:

            score += 20

            observations.append(
                "MACD is above its signal line."
            )

        else:

            score -= 20

            observations.append(
                "MACD is below its signal line."
            )

    score = max(0, min(100, score))

    if score >= 70:
        label = "STRONG"
    elif score >= 55:
        label = "POSITIVE"
    elif score <= 30:
        label = "WEAK"
    elif score <= 45:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return score, label, observations
