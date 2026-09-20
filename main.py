"""TATA DTM Driver Training - main application host.

This file only serves the frozen driver-training HTML application.
The application itself continues to use the Supabase configuration embedded
in index.html for authentication and data storage. No PostgreSQL schema is
created or modified by this host service.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"

app = FastAPI(
    title="TATA Motors CV Driver Training",
    version="V40",
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "ok": True,
        "application": "TATA Motors CV Driver Training",
        "version": "V40",
        "index_exists": INDEX_FILE.exists(),
    }


@app.get("/")
def home():
    if not INDEX_FILE.exists():
        return {"ok": False, "error": "index.html not found"}
    return FileResponse(INDEX_FILE, media_type="text/html; charset=utf-8")


@app.get("/index.html")
def index():
    return home()


@app.get("/dashboard")
def dashboard_redirect():
    # Keep accidental /dashboard visits from producing a 404 on the main app.
    return RedirectResponse(url="/", status_code=307)
