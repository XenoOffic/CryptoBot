from pydantic import BaseModel
from typing import List


class MarketSnapshot(BaseModel):
    symbol: str
    name: str
    price: float
    change_24h: float
    volume_24h: float
    market_cap: float


class Candle(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class IndicatorSnapshot(BaseModel):
    rsi: float | None = None

    macd: float | None = None
    macd_signal: float | None = None
    macd_histogram: float | None = None

    ema_20: float | None = None
    ema_50: float | None = None
    ema_200: float | None = None

    sma_20: float | None = None
    sma_50: float | None = None
    sma_200: float | None = None

    bollinger_upper: float | None = None
    bollinger_middle: float | None = None
    bollinger_lower: float | None = None

    atr: float | None = None
