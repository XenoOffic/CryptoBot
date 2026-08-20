from collections.abc import Sequence

from app.models.market import Candle


def validate_candles(
    candles: Sequence[Candle],
) -> list[Candle]:

    if not candles:
        raise ValueError(
            "Historical candle data is empty."
        )

    validated: list[Candle] = []

    previous_timestamp = None

    for candle in candles:

        if candle.open <= 0:
            raise ValueError(
                "Candle open price must be positive."
            )

        if candle.high <= 0:
            raise ValueError(
                "Candle high price must be positive."
            )

        if candle.low <= 0:
            raise ValueError(
                "Candle low price must be positive."
            )

        if candle.close <= 0:
            raise ValueError(
                "Candle close price must be positive."
            )

        if candle.high < candle.low:
            raise ValueError(
                "Candle high cannot be below low."
            )

        if candle.high < max(
            candle.open,
            candle.close,
        ):
            raise ValueError(
                "Candle high is inconsistent."
            )

        if candle.low > min(
            candle.open,
            candle.close,
        ):
            raise ValueError(
                "Candle low is inconsistent."
            )

        if candle.volume < 0:
            raise ValueError(
                "Candle volume cannot be negative."
            )

        if (
            previous_timestamp is not None
            and candle.timestamp <= previous_timestamp
        ):
            raise ValueError(
                "Candle timestamps must be strictly increasing."
            )

        previous_timestamp = candle.timestamp

        validated.append(candle)

    return validated
