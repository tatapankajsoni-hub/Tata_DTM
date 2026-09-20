from pathlib import Path
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://zamtoehvbdmridqaqqpi.supabase.co").strip().rstrip("/")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", "").strip()

app = FastAPI(title="Tata Motors DTM Driver Training", version="V40.2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "HEAD", "OPTIONS"],
    allow_headers=["*"]
)


def rendered_index() -> str:
    html = INDEX.read_text(encoding="utf-8")
    html = html.replace("__SUPABASE_URL__", SUPABASE_URL)
    html = html.replace("__SUPABASE_PUBLISHABLE_KEY__", SUPABASE_PUBLISHABLE_KEY)
    return html


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "Tata Motors DTM Driver Training",
        "version": "V40.2",
        "supabase_url_configured": bool(SUPABASE_URL),
        "supabase_publishable_key_configured": bool(SUPABASE_PUBLISHABLE_KEY),
    }


@app.get("/api/config")
def config():
    return JSONResponse({
        "ok": True,
        "supabase_url": SUPABASE_URL,
        "supabase_publishable_key_configured": bool(SUPABASE_PUBLISHABLE_KEY),
    })


@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(rendered_index())


@app.get("/index.html", response_class=HTMLResponse)
def index():
    return HTMLResponse(rendered_index())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
