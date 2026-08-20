from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
)

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates


from app.data.market_data import (
    get_market_snapshot,
)

from app.services.analysis_service import (
    analyze_crypto,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"

STATIC_DIR = FRONTEND_DIR / "static"

TEMPLATES_DIR = FRONTEND_DIR / "templates"


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Cryptolytics",
    description=(
        "Cryptocurrency market analysis "
        "and quantitative intelligence engine."
    ),
    version="0.3.0",
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
# WEB ROUTES
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
# HEALTH
# ============================================================

@app.get("/api/health")
async def health():

    return {
        "status": "online",
        "service": "cryptolytics",
        "version": "0.3.0",
    }


# ============================================================
# MARKET DATA
# ============================================================

@app.get("/api/market/{symbol}")
async def market(
    symbol: str,
):

    try:

        snapshot = await get_market_snapshot(
            symbol
        )

        return snapshot

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print(
            f"[MARKET ERROR] {error}"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Market data provider "
                "unavailable."
            ),
        )


# ============================================================
# FULL ANALYSIS
# ============================================================

@app.get("/api/analysis/{symbol}")
async def analysis(
    symbol: str,
):

    try:

        result = await analyze_crypto(
            symbol
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print(
            f"[ANALYSIS ERROR] {error}"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Unable to perform "
                "market analysis."
            ),
        )
