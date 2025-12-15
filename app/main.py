from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone

from app.scraper.static import static_scrape
from app.scraper.js import js_scrape
from app.scraper.parser import parse_html

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/scrape")
async def scrape(payload: dict):
    url = payload.get("url")

    if not url or not url.startswith("http"):
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid URL (only http/https allowed)"}
        )

    errors = []
    interactions = {"clicks": [], "scrolls": 0, "pages": [url]}

    #Static first
    try:
        html, meta, text_len = static_scrape(url)
        strategy = "static"
    except Exception as e:
        errors.append({"message": str(e), "phase": "fetch"})
        html, meta, text_len = "", {}, 0

    #JS fallback 
    if text_len < 300:
        try:
            html, interactions = await js_scrape(url)
            strategy = "js"
        except Exception as e:
            errors.append({"message": str(e), "phase": "render"})

    sections = parse_html(html, url)

    if not sections:
        errors.append({"message": "No sections parsed", "phase": "parse"})

    result = {
        "url": url,
        "scrapedAt": datetime.now(timezone.utc).isoformat(),
        "meta": meta,
        "sections": sections,
        "interactions": interactions,
        "errors": errors
    }

    return {"result": result}
