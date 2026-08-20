from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
)

from fastapi.staticfiles import (
    StaticFiles,
)

from fastapi.templating import (
    Jinja2Templates,
)


from app.data.market_data import (
    get_historical_data,
    get_market_snapshot,
)

from app.analysis.indicators import (
    calculate_indicators,
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


FRONTEND_DIR = (
    BASE_DIR
    / "frontend"
)


STATIC_DIR = (
    FRONTEND_DIR
    / "static"
)


TEMPLATES_DIR = (
    FRONTEND_DIR
    / "templates"
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Cryptolytics",
    description=(
        "Cryptocurrency market "
        "analysis engine"
    ),
    version="0.4.0",
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=STATIC_DIR
    ),
    name="static",
)


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=TEMPLATES_DIR
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

        # Intentionally disabled.
        "trading_engine": "disabled",
        "paper_trading": "disabled",
        "live_trading": "disabled",

        "version": "0.4.0",
    }


# ============================================================
# MARKET SNAPSHOT
# ============================================================

@app.get(
    "/api/market/{symbol}"
)
async def market(
    symbol: str,
):

    try:

        snapshot = (
            await get_market_snapshot(
                symbol
            )
        )

        return snapshot

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except RuntimeError as error:

        print(
            f"[MARKET ERROR] {error}"
        )

        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"[UNEXPECTED MARKET ERROR] "
            f"{error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected internal "
                "server error."
            ),
        ) from error


# ============================================================
# FULL ANALYSIS
# ============================================================

@app.get(
    "/api/analysis/{symbol}"
)
async def analysis(
    symbol: str,
):

    try:

        # ----------------------------------------------------
        # MARKET DATA
        # ----------------------------------------------------

        market = (
            await get_market_snapshot(
                symbol
            )
        )

        # ----------------------------------------------------
        # HISTORICAL DATA
        # ----------------------------------------------------

        candles = (
            await get_historical_data(
                symbol,
                days=30,
            )
        )

        # ----------------------------------------------------
        # TECHNICAL INDICATORS
        # ----------------------------------------------------

        indicators = (
            calculate_indicators(
                candles
            )
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return {
            "market": market,
            "candles": candles,
            "indicators": indicators,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except RuntimeError as error:

        print(
            f"[ANALYSIS ERROR] {error}"
        )

        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"[UNEXPECTED ANALYSIS ERROR] "
            f"{error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to complete "
                "cryptocurrency analysis."
            ),
        ) from error
