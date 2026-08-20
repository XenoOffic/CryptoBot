from __future__ import annotations

from typing import Any

import httpx

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

    try:

        return MarketSnapshot(
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


# ============================================================
# HISTORICAL VOLUME DATA
# ============================================================

async def _get_historical_volumes(
    coin_id: str,
    days: int,
) -> list[tuple[int, float]]:

    url = (
        f"{COINGECKO_URL}/coins/"
        f"{coin_id}/market_chart"
    )

    params = {
        "vs_currency": "usd",
        "days": days,
    }

    data = await _get(
        url,
        params,
        timeout=20,
    )

    volumes = data.get(
        "total_volumes",
        [],
    )

    result: list[
        tuple[int, float]
    ] = []

    for row in volumes:

        if not isinstance(
            row,
            list,
        ):

            continue

        if len(row) < 2:
            continue

        try:

            timestamp = int(
                row[0]
            )

            volume = float(
                row[1]
            )

            result.append(
                (
                    timestamp,
                    volume,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            continue

    return result


# ============================================================
# MATCH VOLUME TO CANDLE
# ============================================================

def _find_nearest_volume(
    candle_timestamp: int,
    volumes: list[tuple[int, float]],
) -> float:

    if not volumes:
        return 0.0

    nearest_timestamp, nearest_volume = min(
        volumes,
        key=lambda item: abs(
            item[0]
            - candle_timestamp
        ),
    )

    return float(
        nearest_volume
    )


# ============================================================
# HISTORICAL OHLC + VOLUME
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

    normalized = (
        symbol
        .upper()
        .strip()
    )

    coin_id = get_coin_id(
        normalized
    )


    # --------------------------------------------------------
    # OHLC DATA
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
    # FETCH VOLUMES
    # --------------------------------------------------------

    try:

        volumes = (
            await _get_historical_volumes(
                coin_id,
                days,
            )
        )

    except RuntimeError as error:

        # Volume is supplementary data.
        # If unavailable, candles remain usable.
        print(
            "[VOLUME WARNING]",
            error,
        )

        volumes = []


    # --------------------------------------------------------
    # BUILD CANDLES
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


        # ----------------------------------------------------
        # MATCH VOLUME
        # ----------------------------------------------------

        volume = (
            _find_nearest_volume(
                timestamp,
                volumes,
            )
        )


        # ----------------------------------------------------
        # CREATE CANDLE
        # ----------------------------------------------------

        candles.append(
            Candle(

                timestamp=timestamp,

                open=open_price,

                high=high,

                low=low,

                close=close,

                volume=volume,
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
    # REMOVE DUPLICATE TIMESTAMPS
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


    return unique_candles
