from __future__ import annotations

from typing import Any

import httpx

from app.data.cache import (
    market_cache,
    historical_cache,
)

from app.models.market import (
    Candle,
    MarketSnapshot,
)


# ============================================================
# CONFIGURATION
# ============================================================

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3"
)

REQUEST_TIMEOUT = 20.0

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Cryptolytics/0.5",
}


# ============================================================
# SUPPORTED ASSETS
# ============================================================

COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "DOGECOIN": "dogecoin",
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
    params: dict[str, Any],
    timeout: float = REQUEST_TIMEOUT,
) -> Any:

    try:

        async with httpx.AsyncClient(
            timeout=timeout,
            headers=HEADERS,
        ) as client:

            response = await client.get(
                url,
                params=params,
            )

            response.raise_for_status()

            return response.json()

    except httpx.HTTPStatusError as error:

        status_code = (
            error.response.status_code
        )

        if status_code == 429:

            raise RuntimeError(
                "Market data provider "
                "rate limit reached."
            ) from error

        raise RuntimeError(
            "Market data provider "
            f"returned HTTP {status_code}."
        ) from error

    except httpx.RequestError as error:

        raise RuntimeError(
            "Unable to connect to "
            "market data provider."
        ) from error


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

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    cache_key = (
        f"market:{normalized}"
    )

    cached = market_cache.get(
        cache_key
    )

    if cached is not None:
        return cached

    # --------------------------------------------------------
    # COIN ID
    # --------------------------------------------------------

    coin_id = get_coin_id(
        normalized
    )

    # --------------------------------------------------------
    # REQUEST
    # --------------------------------------------------------

    url = (
        f"{COINGECKO_URL}/coins/markets"
    )

    params = {
        "vs_currency": "usd",
        "ids": coin_id,
        "price_change_percentage": "24h",
    }

    data = await _get(
        url,
        params,
        timeout=15,
    )

    if not data:

        raise ValueError(
            f"No market data returned "
            f"for {normalized}."
        )

    coin = data[0]

    # --------------------------------------------------------
    # BUILD SNAPSHOT
    # --------------------------------------------------------

    try:

        snapshot = MarketSnapshot(
            symbol=normalized,

            name=str(
                coin["name"]
            ),

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

    except (
        KeyError,
        TypeError,
        ValueError,
    ) as error:

        raise RuntimeError(
            "Invalid market data "
            "received from provider."
        ) from error

    # --------------------------------------------------------
    # SAVE TO CACHE
    # --------------------------------------------------------

    market_cache.set(
        cache_key,
        snapshot,
    )

    return snapshot


# ============================================================
# HISTORICAL OHLC DATA
# ============================================================

async def get_historical_data(
    symbol: str,
    days: int = 30,
) -> list[Candle]:

    # --------------------------------------------------------
    # VALIDATE DAYS
    # --------------------------------------------------------

    if days < 1:

        raise ValueError(
            "days must be at least 1."
        )

    if days > 365:

        raise ValueError(
            "days cannot exceed 365."
        )

    # --------------------------------------------------------
    # NORMALIZE SYMBOL
    # --------------------------------------------------------

    normalized = (
        symbol
        .upper()
        .strip()
    )

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    cache_key = (
        f"historical:{normalized}:{days}"
    )

    cached = historical_cache.get(
        cache_key
    )

    if cached is not None:
        return cached

    # --------------------------------------------------------
    # COIN ID
    # --------------------------------------------------------

    coin_id = get_coin_id(
        normalized
    )

    # --------------------------------------------------------
    # OHLC ENDPOINT
    # --------------------------------------------------------

    ohlc_url = (
        f"{COINGECKO_URL}/coins/"
        f"{coin_id}/ohlc"
    )

    ohlc_params = {
        "vs_currency": "usd",
        "days": days,
    }

    # --------------------------------------------------------
    # FETCH OHLC
    # --------------------------------------------------------

    ohlc_data = await _get(
        ohlc_url,
        ohlc_params,
        timeout=20,
    )

    if not ohlc_data:

        raise ValueError(
            f"No historical data returned "
            f"for {normalized}."
        )

    # --------------------------------------------------------
    # BUILD CANDLES
    #
    # IMPORTANT:
    # Historical volume is intentionally not requested.
    # This avoids an additional CoinGecko API request and
    # reduces the probability of hitting the rate limit.
    # --------------------------------------------------------

    candles: list[Candle] = []

    for row in ohlc_data:

        if not isinstance(
            row,
            list,
        ):

            continue

        if len(row) < 5:
            continue

        # ----------------------------------------------------
        # PARSE OHLC
        # ----------------------------------------------------

        try:

            timestamp = int(
                row[0]
            )

            open_price = float(
                row[1]
            )

            high = float(
                row[2]
            )

            low = float(
                row[3]
            )

            close = float(
                row[4]
            )

        except (
            TypeError,
            ValueError,
        ):

            continue

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if (
            open_price < 0
            or high < 0
            or low < 0
            or close < 0
        ):

            continue

        if high < low:

            continue

        if (
            open_price > high
            or open_price < low
        ):

            continue

        if (
            close > high
            or close < low
        ):

            continue

        # ----------------------------------------------------
        # CREATE CANDLE
        #
        # Volume is unavailable because we intentionally
        # avoid the additional market_chart API request.
        # ----------------------------------------------------

        candles.append(
            Candle(

                timestamp=timestamp,

                open=open_price,

                high=high,

                low=low,

                close=close,

                volume=0.0,
            )
        )

    # --------------------------------------------------------
    # VALIDATE RESULT
    # --------------------------------------------------------

    if not candles:

        raise ValueError(
            "No valid candles were "
            "returned by the provider."
        )

    # --------------------------------------------------------
    # SORT CHRONOLOGICALLY
    # --------------------------------------------------------

    candles.sort(
        key=lambda candle:
        candle.timestamp
    )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    unique_candles: list[
        Candle
    ] = []

    seen_timestamps: set[int] = set()

    for candle in candles:

        if candle.timestamp in (
            seen_timestamps
        ):

            continue

        seen_timestamps.add(
            candle.timestamp
        )

        unique_candles.append(
            candle
        )

    # --------------------------------------------------------
    # SAVE TO CACHE
    # --------------------------------------------------------

    historical_cache.set(
        cache_key,
        unique_candles,
    )

    return unique_candles
