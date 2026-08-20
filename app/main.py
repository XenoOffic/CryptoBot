from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    Request,
)

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.analysis.indicators import (
    calculate_indicators,
)

from app.data.market_data import (
    get_historical_data,
    get_market_snapshot,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

FRONTEND_DIR = BASE_DIR / "frontend"

STATIC_DIR = FRONTEND_DIR / "static"

TEMPLATES_DIR = FRONTEND_DIR / "templates"


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Cryptolytics",
    description=(
        "Cryptocurrency market analysis engine"
    ),
    version="0.4.0",
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=STATIC_DIR,
    ),
    name="static",
)


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=TEMPLATES_DIR,
)


# ============================================================
# DASHBOARD
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def dashboard(
    request: Request,
):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
async def health():

    return {
        "status": "online",
        "service": "cryptolytics",
        "version": "0.4.0",
    }


# ============================================================
# SYSTEM STATUS
# ============================================================

@app.get("/api/system")
async def system():

    return {
        "service": "cryptolytics",
        "status": "online",

        "analysis_engine": "online",

        # Trading remains intentionally disabled.
        "trading_engine": "disabled",
        "paper_trading": "disabled",
        "live_trading": "disabled",

        "version": "0.4.0",
    }


# ============================================================
# MARKET SNAPSHOT
# ============================================================

@app.get(
    "/api/market/{symbol}",
)
async def market(
    symbol: str,
):

    try:

        snapshot = await get_market_snapshot(
            symbol,
        )

        return snapshot

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except RuntimeError as error:

        print(
            f"[MARKET ERROR] {error}",
        )

        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"[UNEXPECTED MARKET ERROR] "
            f"{error}",
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected internal "
                "server error."
            ),
        ) from error


# ============================================================
# CANDLE DATA
# ============================================================

@app.get(
    "/api/candles/{symbol}",
)
async def candles(
    symbol: str,

    days: int = Query(
        default=30,
        ge=1,
        le=365,
        description=(
            "Historical candle period "
            "in days."
        ),
    ),
):

    try:

        data = await get_historical_data(
            symbol,
            days=days,
        )

        return {
            "symbol": symbol.upper(),
            "period_days": days,
            "count": len(data),
            "candles": data,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except RuntimeError as error:

        print(
            f"[CANDLE ERROR] {error}",
        )

        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"[UNEXPECTED CANDLE ERROR] "
            f"{error}",
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to retrieve "
                "candle data."
            ),
        ) from error


# ============================================================
# FULL ANALYSIS
# ============================================================

@app.get(
    "/api/analysis/{symbol}",
)
async def analysis(
    symbol: str,

    days: int = Query(
        default=30,
        ge=1,
        le=365,
        description=(
            "Historical analysis period "
            "in days."
        ),
    ),
):

    try:

        # ----------------------------------------------------
        # CURRENT MARKET DATA
        # ----------------------------------------------------

        market_data = (
            await get_market_snapshot(
                symbol,
            )
        )

        # ----------------------------------------------------
        # HISTORICAL DATA
        # ----------------------------------------------------

        historical_candles = (
            await get_historical_data(
                symbol,
                days=days,
            )
        )

        # ----------------------------------------------------
        # TECHNICAL INDICATORS
        # ----------------------------------------------------

        indicators = calculate_indicators(
            historical_candles,
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return {
            "symbol": market_data.symbol,

            "period_days": days,

            "market": market_data,

            "candles": historical_candles,

            "indicators": indicators,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except RuntimeError as error:

        print(
            f"[ANALYSIS ERROR] {error}",
        )

        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"[UNEXPECTED ANALYSIS ERROR] "
            f"{error}",
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to complete "
                "cryptocurrency analysis."
            ),
        ) from error
