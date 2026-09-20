from pathlib import Path
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

app = FastAPI(title="Tata Motors DTM Driver Training", version="V40.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "HEAD", "OPTIONS"],
    allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"ok": True, "service": "Tata Motors DTM Driver Training", "version": "V40.1"}

@app.get("/api/config")
def config():
    return JSONResponse({"ok": True, "supabase_configured_in_html": True})

@app.get("/")
def home():
    return FileResponse(INDEX, media_type="text/html")

@app.get("/index.html")
def index():
    return FileResponse(INDEX, media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
