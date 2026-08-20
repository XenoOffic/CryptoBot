from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class MarketSnapshot(BaseModel):
    """
    Current market information for a cryptocurrency.
    """

    symbol: str = Field(
        min_length=1,
        max_length=20,
    )

    name: str = Field(
        min_length=1,
    )

    price: float = Field(
        gt=0,
    )

    change_24h: float

    volume_24h: float = Field(
        ge=0,
    )

    market_cap: float = Field(
        ge=0,
    )

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(
        cls,
        value: str,
    ) -> str:

        return value.strip().upper()


class Candle(BaseModel):
    """
    OHLCV market candle.
    """

    timestamp: int = Field(
        gt=0,
    )

    open: float = Field(
        gt=0,
    )

    high: float = Field(
        gt=0,
    )

    low: float = Field(
        gt=0,
    )

    close: float = Field(
        gt=0,
    )

    volume: float = Field(
        ge=0,
    )

    @field_validator(
        "high"
    )
    @classmethod
    def validate_high(
        cls,
        value: float,
    ) -> float:

        return value

    def timestamp_datetime(
        self,
    ) -> datetime:
        """
        Return candle timestamp as UTC datetime.
        """

        timestamp = self.timestamp

        if timestamp > 10_000_000_000:
            timestamp /= 1000

        return datetime.fromtimestamp(
            timestamp,
            tz=timezone.utc,
        )
