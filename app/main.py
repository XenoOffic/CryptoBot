from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.data.market_data import get_market_snapshot

from app.data.market_data import (
    get_historical_data,
    get_market_snapshot,
)

from app.analysis.indicators import (
    calculate_indicators,
)


BASE_DIR = Path(__file__).resolve().parent.parent


app = FastAPI(
    title="Cryptolytics",
    description="Cryptocurrency market analysis engine",
    version="0.2.0",
)


app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "frontend" / "static"
    ),
    name="static",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "frontend" / "templates"
)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@app.get("/api/health")
async def health():

    return {
        "status": "online",
        "service": "cryptolytics",
        "version": "0.2.0",
    }


@app.get("/api/market/{symbol}")
async def market(symbol: str):

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

    except Exception:

        raise HTTPException(
            status_code=502,
            detail="Market data provider unavailable.",
        )


@app.get("/api/analysis/{symbol}")
async def analysis(symbol: str):

    try:

        market = await get_market_snapshot(
            symbol
        )

        candles = await get_historical_data(
            symbol,
            days=30,
        )

        indicators = calculate_indicators(
            candles
        )

        return {
            "market": market,
            "candles": candles,
            "indicators": indicators,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print(
            f"Analysis error: {error}"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Unable to retrieve "
                "analysis data."
            ),
        )
