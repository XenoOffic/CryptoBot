from typing import Sequence

from app.models.market import Candle


def _find_swing_highs(
    candles: Sequence[Candle],
    window: int = 2,
) -> list[float]:

    highs = []

    for i in range(
        window,
        len(candles) - window,
    ):

        current = candles[i].high

        left = [
            candles[j].high
            for j in range(
                i - window,
                i,
            )
        ]

        right = [
            candles[j].high
            for j in range(
                i + 1,
                i + window + 1,
            )
        ]

        if all(current > value for value in left) and \
           all(current > value for value in right):

            highs.append(current)

    return highs


def _find_swing_lows(
    candles: Sequence[Candle],
    window: int = 2,
) -> list[float]:

    lows = []

    for i in range(
        window,
        len(candles) - window,
    ):

        current = candles[i].low

        left = [
            candles[j].low
            for j in range(
                i - window,
                i,
            )
        ]

        right = [
            candles[j].low
            for j in range(
                i + 1,
                i + window + 1,
            )
        ]

        if all(current < value for value in left) and \
           all(current < value for value in right):

            lows.append(current)

    return lows


def _cluster_levels(
    levels: list[float],
    tolerance: float = 0.01,
) -> list[float]:

    if not levels:
        return []

    sorted_levels = sorted(levels)

    clusters: list[list[float]] = [
        [sorted_levels[0]]
    ]

    for level in sorted_levels[1:]:

        cluster = clusters[-1]

        average = sum(cluster) / len(cluster)

        difference = abs(
            level - average
        ) / average

        if difference <= tolerance:
            cluster.append(level)
        else:
            clusters.append([level])

    return [
        sum(cluster) / len(cluster)
        for cluster in clusters
    ]


def find_support_resistance(
    candles: Sequence[Candle],
    current_price: float,
):
    if len(candles) < 10:
        return {
            "support": [],
            "resistance": [],
        }

    swing_highs = _find_swing_highs(
        candles
    )

    swing_lows = _find_swing_lows(
        candles
    )

    resistance = _cluster_levels(
        swing_highs
    )

    support = _cluster_levels(
        swing_lows
    )

    support = sorted(
        [
            level
            for level in support
            if level < current_price
        ],
        reverse=True,
    )

    resistance = sorted(
        [
            level
            for level in resistance
            if level > current_price
        ]
    )

    return {
        "support": support[:5],
        "resistance": resistance[:5],
    }


def analyze_market_structure(
    candles: Sequence[Candle],
):
    if len(candles) < 10:
        return (
            50.0,
            "NEUTRAL",
            [
                "Not enough historical "
                "data to determine market structure."
            ],
        )

    swing_highs = _find_swing_highs(
        candles
    )

    swing_lows = _find_swing_lows(
        candles
    )

    observations = []

    score = 50.0

    # --------------------------------------------------------
    # HIGH STRUCTURE
    # --------------------------------------------------------

    if len(swing_highs) >= 2:

        previous_high = swing_highs[-2]
        latest_high = swing_highs[-1]

        if latest_high > previous_high:

            score += 15

            observations.append(
                "Recent swing highs are rising."
            )

        elif latest_high < previous_high:

            score -= 15

            observations.append(
                "Recent swing highs are falling."
            )

    # --------------------------------------------------------
    # LOW STRUCTURE
    # --------------------------------------------------------

    if len(swing_lows) >= 2:

        previous_low = swing_lows[-2]
        latest_low = swing_lows[-1]

        if latest_low > previous_low:

            score += 20

            observations.append(
                "Recent swing lows are rising."
            )

        elif latest_low < previous_low:

            score -= 20

            observations.append(
                "Recent swing lows are falling."
            )

    # --------------------------------------------------------
    # LABEL
    # --------------------------------------------------------

    score = max(
        0,
        min(100, score),
    )

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

    if not observations:

        observations.append(
            "Market structure is currently "
            "inconclusive."
        )

    return (
        score,
        label,
        observations,
      )
