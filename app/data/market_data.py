import httpx

from app.models.market import (
    MarketSnapshot,
    Candle,
)

from app.data.cache import (
    market_cache,
    historical_cache,
)

from app.data.normalizer import (
    normalize_symbol,
)

from app.data.validators import (
    validate_candles,
)


# ============================================================
# CONFIGURATION
# ============================================================

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3"
)


REQUEST_TIMEOUT = httpx.Timeout(
    connect=5.0,
    read=20.0,
    write=10.0,
    pool=5.0,
)


# ============================================================
# SUPPORTED COINS
# ============================================================

COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
}


# ============================================================
# COIN LOOKUP
# ============================================================

def get_coin_id(
    symbol: str,
) -> str:

    symbol = normalize_symbol(
        symbol
    )

    if symbol not in COIN_IDS:

        raise ValueError(
            f"Unsupported cryptocurrency: {symbol}"
        )

    return COIN_IDS[symbol]


# ============================================================
# MARKET SNAPSHOT
# ============================================================

async def get_market_snapshot(
    symbol: str,
) -> MarketSnapshot:

    symbol = normalize_symbol(
        symbol
    )

    coin_id = get_coin_id(
        symbol
    )

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    cache_key = (
        f"market:{symbol}"
    )

    cached = market_cache.get(
        cache_key
    )

    if cached is not None:

        return cached

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

    try:

        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT
        ) as client:

            response = await client.get(
                url,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

    except httpx.TimeoutException as error:

        raise RuntimeError(
            "CoinGecko request timed out."
        ) from error

    except httpx.HTTPStatusError as error:

        raise RuntimeError(
            "CoinGecko returned an HTTP error."
        ) from error

    except httpx.HTTPError as error:

        raise RuntimeError(
            "Unable to connect to CoinGecko."
        ) from error

    # --------------------------------------------------------
    # RESPONSE VALIDATION
    # --------------------------------------------------------

    if not data:

        raise ValueError(
            f"No market data returned for {symbol}"
        )

    coin = data[0]

    try:

        snapshot = MarketSnapshot(

            symbol=symbol,

            name=coin["name"],

            price=float(
                coin["current_price"]
            ),

            change_24h=float(
                coin.get(
                    "price_change_percentage_24h"
                )
                or 0
            ),

            volume_24h=float(
                coin.get(
                    "total_volume"
                )
                or 0
            ),

            market_cap=float(
                coin.get(
                    "market_cap"
                )
                or 0
            ),

        )

    except (
        KeyError,
        TypeError,
        ValueError,
    ) as error:

        raise RuntimeError(
            "Invalid market data returned "
            "by CoinGecko."
        ) from error

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    market_cache.set(
        cache_key,
        snapshot,
    )

    return snapshot


# ============================================================
# HISTORICAL OHLC
# ============================================================

async def get_historical_data(
    symbol: str,
    days: int = 30,
) -> list[Candle]:

    symbol = normalize_symbol(
        symbol
    )

    coin_id = get_coin_id(
        symbol
    )

    # --------------------------------------------------------
    # VALIDATE DAYS
    # --------------------------------------------------------

    if days <= 0:

        raise ValueError(
            "days must be greater than zero."
        )

    if days > 365:

        raise ValueError(
            "days cannot exceed 365."
        )

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    cache_key = (
        f"historical:{symbol}:{days}"
    )

    cached = historical_cache.get(
        cache_key
    )

    if cached is not None:

        return cached

    # --------------------------------------------------------
    # REQUEST
    # --------------------------------------------------------

    url = (
        f"{COINGECKO_URL}/coins/"
        f"{coin_id}/ohlc"
    )

    params = {
        "vs_currency": "usd",
        "days": days,
    }

    try:

        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT
        ) as client:

            response = await client.get(
                url,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

    except httpx.TimeoutException as error:

        raise RuntimeError(
            "CoinGecko historical data "
            "request timed out."
        ) from error

    except httpx.HTTPStatusError as error:

        raise RuntimeError(
            "CoinGecko returned an HTTP error "
            "while retrieving historical data."
        ) from error

    except httpx.HTTPError as error:

        raise RuntimeError(
            "Unable to retrieve historical "
            "data from CoinGecko."
        ) from error

    # --------------------------------------------------------
    # RESPONSE VALIDATION
    # --------------------------------------------------------

    if not data:

        raise ValueError(
            f"No historical data returned "
            f"for {symbol}."
        )

    candles: list[Candle] = []

    # --------------------------------------------------------
    # PARSE OHLC
    # --------------------------------------------------------

    for row in data:

        if not isinstance(
            row,
            list,
        ):

            continue

        if len(row) < 5:

            continue

        (
            timestamp,
            open_price,
            high,
            low,
            close,
        ) = row[:5]

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
                # does not provide volume.
                volume=0.0,

            )

            candles.append(
                candle
            )

        except (
            TypeError,
            ValueError,
        ):

            continue

    # --------------------------------------------------------
    # VALIDATE CANDLES
    # --------------------------------------------------------

    candles = validate_candles(
        candles
    )

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    historical_cache.set(
        cache_key,
        candles,
    )

    return candles
