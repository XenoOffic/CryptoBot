from __future__ import annotations

from typing import Any

from app.models.market import Candle


# ============================================================
# BASIC HELPERS
# ============================================================

def _closes(candles: list[Candle]) -> list[float]:
    return [float(candle.close) for candle in candles]


def _highs(candles: list[Candle]) -> list[float]:
    return [float(candle.high) for candle in candles]


def _lows(candles: list[Candle]) -> list[float]:
    return [float(candle.low) for candle in candles]


def _volumes(candles: list[Candle]) -> list[float]:
    return [float(candle.volume) for candle in candles]


# ============================================================
# SMA SERIES
# ============================================================

def calculate_sma_series(
    values: list[float],
    period: int,
) -> list[float | None]:

    if period <= 0:
        raise ValueError(
            "SMA period must be greater than zero."
        )

    result: list[float | None] = []

    for index in range(len(values)):

        if index + 1 < period:
            result.append(None)
            continue

        window = values[
            index + 1 - period:
            index + 1
        ]

        result.append(
            sum(window) / period
        )

    return result


def calculate_sma(
    values: list[float],
    period: int,
) -> float | None:

    series = calculate_sma_series(
        values,
        period,
    )

    if not series:
        return None

    return series[-1]


# ============================================================
# EMA SERIES
# ============================================================

def calculate_ema_series(
    values: list[float],
    period: int,
) -> list[float | None]:

    if period <= 0:
        raise ValueError(
            "EMA period must be greater than zero."
        )

    result: list[float | None] = []

    if len(values) < period:
        return [None] * len(values)

    multiplier = 2 / (period + 1)

    initial_ema = (
        sum(values[:period]) / period
    )

    for index in range(period - 1):

        result.append(None)

    result.append(initial_ema)

    ema = initial_ema

    for index in range(period, len(values)):

        ema = (
            (values[index] - ema)
            * multiplier
        ) + ema

        result.append(ema)

    return result


def calculate_ema(
    values: list[float],
    period: int,
) -> float | None:

    series = calculate_ema_series(
        values,
        period,
    )

    if not series:
        return None

    return series[-1]


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

        gains.append(
            max(change, 0.0)
        )

        losses.append(
            max(-change, 0.0)
        )

    average_gain = (
        sum(gains[:period])
        / period
    )

    average_loss = (
        sum(losses[:period])
        / period
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

        if average_gain == 0:
            return 50.0

        return 100.0

    relative_strength = (
        average_gain
        / average_loss
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
) -> dict[str, Any]:

    if len(values) < slow_period:

        return {
            "macd": None,
            "signal": None,
            "histogram": None,
            "series": {
                "macd": [],
                "signal": [],
                "histogram": [],
            },
        }

    fast_series = calculate_ema_series(
        values,
        fast_period,
    )

    slow_series = calculate_ema_series(
        values,
        slow_period,
    )

    macd_series: list[float | None] = []

    for index in range(len(values)):

        fast = fast_series[index]
        slow = slow_series[index]

        if fast is None or slow is None:
            macd_series.append(None)
        else:
            macd_series.append(
                fast - slow
            )

    valid_macd = [
        value
        for value in macd_series
        if value is not None
    ]

    signal_values = calculate_ema_series(
        valid_macd,
        signal_period,
    )

    signal_series: list[float | None] = []

    valid_index = 0

    for value in macd_series:

        if value is None:
            signal_series.append(None)
            continue

        signal_series.append(
            signal_values[valid_index]
        )

        valid_index += 1

    histogram_series: list[float | None] = []

    for index in range(len(values)):

        macd_value = macd_series[index]
        signal_value = signal_series[index]

        if (
            macd_value is None
            or signal_value is None
        ):
            histogram_series.append(None)
        else:
            histogram_series.append(
                macd_value - signal_value
            )

    current_macd = (
        macd_series[-1]
        if macd_series
        else None
    )

    current_signal = (
        signal_series[-1]
        if signal_series
        else None
    )

    current_histogram = (
        histogram_series[-1]
        if histogram_series
        else None
    )

    return {

        "macd": current_macd,

        "signal": current_signal,

        "histogram": current_histogram,

        "series": {

            "macd": macd_series,

            "signal": signal_series,

            "histogram": histogram_series,
        },
    }


# ============================================================
# BOLLINGER BANDS
# ============================================================

def calculate_bollinger_series(
    values: list[float],
    period: int = 20,
    standard_deviations: float = 2.0,
) -> dict[str, list[float | None]]:

    if period <= 0:
        raise ValueError(
            "Bollinger period must be greater than zero."
        )

    middle: list[float | None] = []
    upper: list[float | None] = []
    lower: list[float | None] = []
    width: list[float | None] = []

    for index in range(len(values)):

        if index + 1 < period:

            middle.append(None)
            upper.append(None)
            lower.append(None)
            width.append(None)

            continue

        window = values[
            index + 1 - period:
            index + 1
        ]

        average = (
            sum(window) / period
        )

        variance = sum(
            (value - average) ** 2
            for value in window
        ) / period

        deviation = variance ** 0.5

        upper_value = (
            average
            + standard_deviations
            * deviation
        )

        lower_value = (
            average
            - standard_deviations
            * deviation
        )

        band_width = None

        if average != 0:

            band_width = (
                (
                    upper_value
                    - lower_value
                )
                / average
            )

        middle.append(average)
        upper.append(upper_value)
        lower.append(lower_value)
        width.append(band_width)

    return {
        "middle": middle,
        "upper": upper,
        "lower": lower,
        "width": width,
    }


def calculate_bollinger_bands(
    values: list[float],
    period: int = 20,
    standard_deviations: float = 2.0,
) -> dict[str, Any]:

    series = calculate_bollinger_series(
        values,
        period,
        standard_deviations,
    )

    return {

        "middle": series["middle"][-1]
        if series["middle"]
        else None,

        "upper": series["upper"][-1]
        if series["upper"]
        else None,

        "lower": series["lower"][-1]
        if series["lower"]
        else None,

        "width": series["width"][-1]
        if series["width"]
        else None,

        "series": series,
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

    if len(candles) < period:
        return None

    true_ranges: list[float] = []

    for index, candle in enumerate(candles):

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

    return (
        sum(
            true_ranges[-period:]
        )
        / period
    )


# ============================================================
# VOLUME
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
# MAIN ANALYSIS
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

    # --------------------------------------------------------
    # MOVING AVERAGES
    # --------------------------------------------------------

    sma20_series = calculate_sma_series(
        closes,
        20,
    )

    sma50_series = calculate_sma_series(
        closes,
        50,
    )

    ema20_series = calculate_ema_series(
        closes,
        20,
    )

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    rsi = calculate_rsi(
        closes,
        14,
    )

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

    macd = calculate_macd(
        closes,
    )

    # --------------------------------------------------------
    # BOLLINGER
    # --------------------------------------------------------

    bollinger = calculate_bollinger_bands(
        closes,
        20,
    )

    # --------------------------------------------------------
    # ATR
    # --------------------------------------------------------

    atr = calculate_atr(
        candles,
        14,
    )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    volume = calculate_volume_analysis(
        candles,
        20,
    )

    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    trend = determine_trend(
        candles,
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "current_price": current_price,

        "moving_averages": {

            "sma_20": sma20_series[-1],

            "sma_50": sma50_series[-1],

            "ema_20": ema20_series[-1],

            "series": {

                "sma_20": sma20_series,

                "sma_50": sma50_series,

                "ema_20": ema20_series,
            },
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
