from typing import Sequence

from app.models.market import (
    Candle,
    IndicatorSnapshot,
)


def closes(candles: Sequence[Candle]) -> list[float]:
    return [c.close for c in candles]


def highs(candles: Sequence[Candle]) -> list[float]:
    return [c.high for c in candles]


def lows(candles: Sequence[Candle]) -> list[float]:
    return [c.low for c in candles]


def sma(
    values: list[float],
    period: int,
) -> float | None:

    if len(values) < period:
        return None

    window = values[-period:]

    return sum(window) / period


def ema_series(
    values: list[float],
    period: int,
) -> list[float]:

    if not values:
        return []

    multiplier = 2 / (period + 1)

    ema = values[0]

    result = [ema]

    for value in values[1:]:

        ema = (
            (value - ema)
            * multiplier
            + ema
        )

        result.append(ema)

    return result


def ema(
    values: list[float],
    period: int,
) -> float | None:

    if len(values) < period:
        return None

    series = ema_series(
        values,
        period,
    )

    return series[-1]


def rsi(
    values: list[float],
    period: int = 14,
) -> float | None:

    if len(values) <= period:
        return None

    gains = []
    losses = []

    for i in range(1, len(values)):

        change = (
            values[i]
            - values[i - 1]
        )

        gains.append(
            max(change, 0)
        )

        losses.append(
            max(-change, 0)
        )

    avg_gain = (
        sum(gains[:period])
        / period
    )

    avg_loss = (
        sum(losses[:period])
        / period
    )

    for i in range(
        period,
        len(gains),
    ):

        avg_gain = (
            (avg_gain * (period - 1))
            + gains[i]
        ) / period

        avg_loss = (
            (avg_loss * (period - 1))
            + losses[i]
        ) / period

    if avg_loss == 0:
        return 100.0

    relative_strength = (
        avg_gain / avg_loss
    )

    return 100 - (
        100 / (1 + relative_strength)
    )


def macd(
    values: list[float],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
):

    if len(values) < slow:
        return None, None, None

    fast_series = ema_series(
        values,
        fast,
    )

    slow_series = ema_series(
        values,
        slow,
    )

    macd_series = []

    for fast_value, slow_value in zip(
        fast_series[-len(slow_series):],
        slow_series,
    ):
        macd_series.append(
            fast_value - slow_value
        )

    signal_series = ema_series(
        macd_series,
        signal,
    )

    return (
        macd_series[-1],
        signal_series[-1],
        (
            macd_series[-1]
            - signal_series[-1]
        ),
    )


def bollinger_bands(
    values: list[float],
    period: int = 20,
    deviations: float = 2.0,
):

    if len(values) < period:
        return None, None, None

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
        + deviations * standard_deviation
    )

    lower = (
        middle
        - deviations * standard_deviation
    )

    return upper, middle, lower


def atr(
    candles: Sequence[Candle],
    period: int = 14,
) -> float | None:

    if len(candles) <= period:
        return None

    true_ranges = []

    for i in range(1, len(candles)):

        current = candles[i]
        previous = candles[i - 1]

        true_range = max(
            current.high - current.low,
            abs(
                current.high
                - previous.close
            ),
            abs(
                current.low
                - previous.close
            ),
        )

        true_ranges.append(
            true_range
        )

    if len(true_ranges) < period:
        return None

    return (
        sum(true_ranges[-period:])
        / period
    )


def calculate_indicators(
    candles: Sequence[Candle],
) -> IndicatorSnapshot:

    values = closes(candles)

    macd_value, macd_signal, macd_histogram = (
        macd(values)
    )

    bb_upper, bb_middle, bb_lower = (
        bollinger_bands(values)
    )

    return IndicatorSnapshot(

        rsi=rsi(values),

        macd=macd_value,
        macd_signal=macd_signal,
        macd_histogram=macd_histogram,

        ema_20=ema(values, 20),
        ema_50=ema(values, 50),
        ema_200=ema(values, 200),

        sma_20=sma(values, 20),
        sma_50=sma(values, 50),
        sma_200=sma(values, 200),

        bollinger_upper=bb_upper,
        bollinger_middle=bb_middle,
        bollinger_lower=bb_lower,

        atr=atr(candles),
  )
