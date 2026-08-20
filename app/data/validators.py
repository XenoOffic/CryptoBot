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

        # ----------------------------------------------------
        # PRICE RELATIONSHIPS
        # ----------------------------------------------------

        if candle.high < candle.low:

            raise ValueError(
                "Candle high cannot be below low."
            )

        if candle.high < candle.open:

            raise ValueError(
                "Candle high cannot be below open."
            )

        if candle.high < candle.close:

            raise ValueError(
                "Candle high cannot be below close."
            )

        if candle.low > candle.open:

            raise ValueError(
                "Candle low cannot be above open."
            )

        if candle.low > candle.close:

            raise ValueError(
                "Candle low cannot be above close."
            )

        # ----------------------------------------------------
        # VOLUME
        # ----------------------------------------------------

        if candle.volume < 0:

            raise ValueError(
                "Candle volume cannot be negative."
            )

        # ----------------------------------------------------
        # CHRONOLOGICAL ORDER
        # ----------------------------------------------------

        if (
            previous_timestamp is not None
            and candle.timestamp
            <= previous_timestamp
        ):

            raise ValueError(
                "Candle timestamps must be "
                "strictly increasing."
            )

        previous_timestamp = (
            candle.timestamp
        )

        validated.append(
            candle
        )

    return validated
