import httpx

from app.models.market import (
    Candle,
    MarketSnapshot,
)


COINGECKO_URL = (
    "https://api.coingecko.com/api/v3"
)


COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
}


# ============================================================
# COIN ID
# ============================================================

def get_coin_id(
    symbol: str,
) -> str:

    normalized = (
        symbol
        .upper()
        .strip()
    )

    if normalized not in COIN_IDS:

        raise ValueError(
            f"Unsupported cryptocurrency: "
            f"{normalized}"
        )

    return COIN_IDS[normalized]


# ============================================================
# HTTP CLIENT
# ============================================================

async def _get(
    url: str,
    params: dict,
    timeout: float = 20,
):

    async with httpx.AsyncClient(
        timeout=timeout,
        headers={
            "Accept": "application/json",
            "User-Agent": (
                "Cryptolytics/0.4"
            ),
        },
    ) as client:

        response = await client.get(
            url,
            params=params,
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# MARKET SNAPSHOT
# ============================================================

async def get_market_snapshot(
    symbol: str,
) -> MarketSnapshot:

    normalized = (
        symbol
        .upper()
        .strip()
    )

    coin_id = get_coin_id(
        normalized
    )

    url = (
        f"{COINGECKO_URL}/coins/markets"
    )

    params = {
        "vs_currency": "usd",
        "ids": coin_id,
        "price_change_percentage": "24h",
    }

    try:

        data = await _get(
            url,
            params,
            timeout=15,
        )

    except httpx.HTTPError as error:

        raise RuntimeError(
            "Market data provider "
            "is unavailable."
        ) from error

    if not data:

        raise ValueError(
            f"No market data returned "
            f"for {normalized}."
        )

    coin = data[0]

    return MarketSnapshot(
        symbol=normalized,

        name=coin["name"],

        price=float(
            coin["current_price"]
        ),

        change_24h=float(
            coin[
                "price_change_percentage_24h"
            ]
            or 0
        ),

        volume_24h=float(
            coin["total_volume"]
            or 0
        ),

        market_cap=float(
            coin["market_cap"]
            or 0
        ),
    )


# ============================================================
# HISTORICAL OHLC
# ============================================================

async def get_historical_data(
    symbol: str,
    days: int = 30,
) -> list[Candle]:

    if days < 1:

        raise ValueError(
            "days must be at least 1."
        )

    if days > 365:

        raise ValueError(
            "days cannot exceed 365."
        )

    coin_id = get_coin_id(
        symbol
    )

    url = (
        f"{COINGECKO_URL}/coins/"
        f"{coin_id}/ohlc"
    )

    params = {
        "vs_currency": "usd",
        "days": days,
    }

    try:

        data = await _get(
            url,
            params,
            timeout=20,
        )

    except httpx.HTTPError as error:

        raise RuntimeError(
            "Historical market data "
            "provider is unavailable."
        ) from error

    if not data:

        raise ValueError(
            f"No historical data returned "
            f"for {symbol.upper()}."
        )

    candles: list[Candle] = []

    for row in data:

        if len(row) < 5:
            continue

        timestamp = row[0]

        open_price = row[1]

        high = row[2]

        low = row[3]

        close = row[4]

        try:

            candle = Candle(
                timestamp=int(
                    timestamp
                ),

                open=float(
                    open_price
                ),

                high=float(
                    high
                ),

                low=float(
                    low
                ),

                close=float(
                    close
                ),

                # CoinGecko's OHLC endpoint
                # does not provide candle volume.
                volume=0.0,
            )

            candles.append(
                candle
            )

        except (TypeError, ValueError):
            continue

    if not candles:

        raise ValueError(
            "No valid candles were "
            "returned by the provider."
        )

    candles.sort(
        key=lambda candle:
        candle.timestamp
    )

    return candles
