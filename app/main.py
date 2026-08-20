from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="Cryptolytics",
    description="Cryptocurrency market analysis engine",
    version="0.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend" / "static"),
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
        "version": "0.1.0",
    }
