import httpx

from app.models.market import (
    MarketSnapshot,
    Candle,
)


COINGECKO_URL = "https://api.coingecko.com/api/v3"


COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
}


def get_coin_id(symbol: str) -> str:

    symbol = symbol.upper().strip()

    if symbol not in COIN_IDS:
        raise ValueError(
            f"Unsupported cryptocurrency: {symbol}"
        )

    return COIN_IDS[symbol]


async def get_market_snapshot(
    symbol: str,
) -> MarketSnapshot:

    coin_id = get_coin_id(symbol)

    url = f"{COINGECKO_URL}/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": coin_id,
        "price_change_percentage": "24h",
    }

    async with httpx.AsyncClient(
        timeout=15
    ) as client:

        response = await client.get(
            url,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

    if not data:
        raise ValueError(
            f"No market data returned for {symbol}"
        )

    coin = data[0]

    return MarketSnapshot(
        symbol=symbol.upper(),
        name=coin["name"],
        price=coin["current_price"],
        change_24h=(
            coin["price_change_percentage_24h"]
            or 0
        ),
        volume_24h=coin["total_volume"] or 0,
        market_cap=coin["market_cap"] or 0,
    )


async def get_historical_data(
    symbol: str,
    days: int = 30,
) -> list[Candle]:

    coin_id = get_coin_id(symbol)

    url = (
        f"{COINGECKO_URL}/coins/"
        f"{coin_id}/ohlc"
    )

    params = {
        "vs_currency": "usd",
        "days": days,
    }

    async with httpx.AsyncClient(
        timeout=20
    ) as client:

        response = await client.get(
            url,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

    candles = []

    for row in data:

        if len(row) < 5:
            continue

        timestamp, open_price, high, low, close = row

        candles.append(
            Candle(
                timestamp=int(timestamp),
                open=float(open_price),
                high=float(high),
                low=float(low),
                close=float(close),
                volume=0.0,
            )
        )

    return candles
