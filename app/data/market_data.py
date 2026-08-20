import httpx

from app.models.market import MarketSnapshot


COINGECKO_URL = "https://api.coingecko.com/api/v3"


COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
}


async def get_market_snapshot(symbol: str) -> MarketSnapshot:
    symbol = symbol.upper().strip()

    if symbol not in COIN_IDS:
        raise ValueError(
            f"Unsupported cryptocurrency: {symbol}"
        )

    coin_id = COIN_IDS[symbol]

    url = f"{COINGECKO_URL}/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": coin_id,
        "price_change_percentage": "24h",
    }

    async with httpx.AsyncClient(timeout=10) as client:

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
        symbol=symbol,
        name=coin["name"],
        price=coin["current_price"],
        change_24h=coin["price_change_percentage_24h"],
        volume_24h=coin["total_volume"],
        market_cap=coin["market_cap"],
    )
