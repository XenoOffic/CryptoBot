from pydantic import BaseModel


class MarketSnapshot(BaseModel):
    symbol: str
    name: str
    price: float
    change_24h: float
    volume_24h: float
    market_cap: float
