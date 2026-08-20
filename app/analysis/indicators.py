from __future__ import annotations

from typing import Any

from app.models.market import Candle


# ============================================================
# BASIC HELPERS
# ============================================================


def _closes(candles: list[Candle]) -> list[float]:
    return [candle.close for candle in candles]


def _highs(candles: list[Candle]) -> list[float]:
    return [candle.high for candle in candles]


def _lows(candles: list[Candle]) -> list[float]:
    return [candle.low for candle in candles]


def _volumes(candles: list[Candle]) -> list[float]:
    return [candle.volume for candle in candles]


# ============================================================
# SIMPLE MOVING AVERAGE
# ============================================================


def calculate_sma(
    values: list[float],
    period: int,
) -> float | None:

    if period <= 0:
        raise ValueError(
            "SMA period must be greater than zero."
        )

    if len(values) < period:
        return None

    window = values[-period:]

    return sum(window) / period


# ============================================================
# EXPONENTIAL MOVING AVERAGE
# ============================================================


def calculate_ema(
    values: list[float],
    period: int,
) -> float | None:

    if period <= 0:
        raise ValueError(
            "EMA period must be greater than zero."
        )

    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)

    ema = sum(values[:period]) / period

    for value in values[period:]:
        ema = (
            (value - ema) * multiplier
        ) + ema

    return ema


# ============================================================
# RSI
# ============================================================


def calculate_rsi(
    values: list[float],
    period: int = 14,
) -> float | None:

    if period <= 0:
        raise ValueError(
            "RSI period must be greater than zero."
        )

    if len(values) <= period:
        return None

    gains: list[float] = []
    losses: list[float] = []

    for index in range(1, len(values)):

        change = (
            values[index]
            - values[index - 1]
        )

        if change > 0:
            gains.append(change)
            losses.append(0.0)

        else:
            gains.append(0.0)
            losses.append(abs(change))

    average_gain = (
        sum(gains[:period]) / period
    )

    average_loss = (
        sum(losses[:period]) / period
    )

    for index in range(
        period,
        len(gains),
    ):

        average_gain = (
            (
                average_gain
                * (period - 1)
            )
            + gains[index]
        ) / period

        average_loss = (
            (
                average_loss
                * (period - 1)
            )
            + losses[index]
        ) / period

    if average_loss == 0:
        return 100.0

    relative_strength = (
        average_gain / average_loss
    )

    return (
        100
        - (
            100
            / (1 + relative_strength)
        )
    )


# ============================================================
# MACD
# ============================================================


def calculate_macd(
    values: list[float],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> dict[str, float | None]:

    if len(values) < slow_period:
        return {
            "macd": None,
            "signal": None,
            "histogram": None,
        }

    fast_ema = calculate_ema(
        values,
        fast_period,
    )

    slow_ema = calculate_ema(
        values,
        slow_period,
    )

    if (
        fast_ema is None
        or slow_ema is None
    ):
        return {
            "macd": None,
            "signal": None,
            "histogram": None,
        }

    macd_value = (
        fast_ema - slow_ema
    )

    # For the first version we calculate
    # the current MACD value.
    #
    # A full historical MACD series will be
    # added when we build the signal engine.

    return {
        "macd": macd_value,
        "signal": None,
        "histogram": None,
    }


# ============================================================
# BOLLINGER BANDS
# ============================================================


def calculate_bollinger_bands(
    values: list[float],
    period: int = 20,
    standard_deviations: float = 2.0,
) -> dict[str, float | None]:

    if period <= 0:
        raise ValueError(
            "Bollinger period must be greater than zero."
        )

    if len(values) < period:
        return {
            "middle": None,
            "upper": None,
            "lower": None,
            "width": None,
        }

    window = values[-period:]

    middle = (
        sum(window) / period
    )

    variance = sum(
        (value - middle) ** 2
        for value in window
    ) / period

    standard_deviation = (
        variance ** 0.5
    )

    upper = (
        middle
        + (
            standard_deviations
            * standard_deviation
        )
    )

    lower = (
        middle
        - (
            standard_deviations
            * standard_deviation
        )
    )

    width = None

    if middle != 0:
        width = (
            (upper - lower)
            / middle
        )

    return {
        "middle": middle,
        "upper": upper,
        "lower": lower,
        "width": width,
    }


# ============================================================
# ATR
# ============================================================


def calculate_atr(
    candles: list[Candle],
    period: int = 14,
) -> float | None:

    if period <= 0:
        raise ValueError(
            "ATR period must be greater than zero."
        )

    if len(candles) <= period:
        return None

    true_ranges: list[float] = []

    for index, candle in enumerate(
        candles
    ):

        if index == 0:

            true_range = (
                candle.high
                - candle.low
            )

        else:

            previous_close = (
                candles[index - 1].close
            )

            true_range = max(
                candle.high - candle.low,
                abs(
                    candle.high
                    - previous_close
                ),
                abs(
                    candle.low
                    - previous_close
                ),
            )

        true_ranges.append(
            true_range
        )

    return sum(
        true_ranges[-period:]
    ) / period


# ============================================================
# VOLUME ANALYSIS
# ============================================================


def calculate_volume_analysis(
    candles: list[Candle],
    period: int = 20,
) -> dict[str, float | None]:

    volumes = _volumes(candles)

    if len(volumes) < period + 1:
        return {
            "current": None,
            "average": None,
            "ratio": None,
        }

    current = volumes[-1]

    historical = volumes[
        -(period + 1):-1
    ]

    average = (
        sum(historical)
        / len(historical)
    )

    ratio = None

    if average > 0:
        ratio = current / average

    return {
        "current": current,
        "average": average,
        "ratio": ratio,
    }


# ============================================================
# TREND
# ============================================================


def determine_trend(
    candles: list[Candle],
) -> str:

    closes = _closes(candles)

    if len(closes) < 50:
        return "insufficient_data"

    sma_20 = calculate_sma(
        closes,
        20,
    )

    sma_50 = calculate_sma(
        closes,
        50,
    )

    current_price = closes[-1]

    if (
        sma_20 is None
        or sma_50 is None
    ):
        return "insufficient_data"

    if (
        current_price > sma_20
        and sma_20 > sma_50
    ):
        return "bullish"

    if (
        current_price < sma_20
        and sma_20 < sma_50
    ):
        return "bearish"

    return "neutral"


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================


def calculate_indicators(
    candles: list[Candle],
) -> dict[str, Any]:

    if not candles:
        raise ValueError(
            "Cannot calculate indicators "
            "without candle data."
        )

    closes = _closes(candles)

    current_price = closes[-1]

    sma_20 = calculate_sma(
        closes,
        20,
    )

    sma_50 = calculate_sma(
        closes,
        50,
    )

    ema_20 = calculate_ema(
        closes,
        20,
    )

    rsi = calculate_rsi(
        closes,
        14,
    )

    macd = calculate_macd(
        closes,
    )

    bollinger = calculate_bollinger_bands(
        closes,
        20,
    )

    atr = calculate_atr(
        candles,
        14,
    )

    volume = calculate_volume_analysis(
        candles,
        20,
    )

    trend = determine_trend(
        candles,
    )

    return {

        "current_price": current_price,

        "moving_averages": {
            "sma_20": sma_20,
            "sma_50": sma_50,
            "ema_20": ema_20,
        },

        "momentum": {
            "rsi_14": rsi,
            "macd": macd,
        },

        "volatility": {
            "atr_14": atr,
            "bollinger_bands": bollinger,
        },

        "volume": volume,

        "trend": trend,
    }
