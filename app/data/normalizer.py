from datetime import datetime, timezone
from typing import Any


def normalize_symbol(symbol: str) -> str:
    """
    Normalize a cryptocurrency symbol.
    """

    if not symbol:
        raise ValueError(
            "Cryptocurrency symbol is required."
        )

    return symbol.strip().upper()


def normalize_timestamp(
    value: Any,
) -> datetime:
    """
    Convert supported timestamp formats
    into timezone-aware UTC datetime.
    """

    if isinstance(value, datetime):

        if value.tzinfo is None:
            return value.replace(
                tzinfo=timezone.utc
            )

        return value.astimezone(
            timezone.utc
        )

    if isinstance(value, (int, float)):

        # Milliseconds
        if value > 10_000_000_000:
            value /= 1000

        return datetime.fromtimestamp(
            value,
            tz=timezone.utc,
        )

    if isinstance(value, str):

        normalized = value.replace(
            "Z",
            "+00:00",
        )

        parsed = datetime.fromisoformat(
            normalized
        )

        if parsed.tzinfo is None:
            parsed = parsed.replace(
                tzinfo=timezone.utc
            )

        return parsed.astimezone(
            timezone.utc
        )

    raise ValueError(
        f"Unsupported timestamp: {value}"
    )


def normalize_number(
    value: Any,
) -> float:

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ) as error:

        raise ValueError(
            f"Invalid numeric value: {value}"
        ) from error
