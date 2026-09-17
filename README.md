# Tata Motors Commercial Vehicles – Driver Training Module | Steps 1–6

## What is included
- **Step 1:** Branded Home / Index screen using the supplied truck image. The original event headline has been removed from the image by cropping the supplied photo for the app hero.
- **Step 2:** Driver registration with driver, licence, vehicle, dealer/workshop and location fields.
- **Step 3:** 8 training modules with English/Hindi UI and module progress.
- **Step 4:** Randomised Pre-Test (10) and Final Assessment (20) with score/result/history.
- **Step 5:** Intelligent question allocation: module balancing for the 20-question final assessment, recent-question avoidance, difficulty metadata and driver attempt history.
- **Step 6:** Trainer/MIS layer plus a FastAPI central API, SQLite demo persistence and PostgreSQL production schema.

## Important source/version note
Training content and the question bank are based on the supplied **Driving Training Module PDF(1).pdf** and the supplied question-bank files. The source contains both BS4/BS6-specific material and dated Tata Samarth information. Validate vehicle/program applicability and any live benefit/claim terms before production release.

## Quick demo (no backend)
Because the frontend is static, the easiest way to run it is with a local web server:

```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in the browser.

## Step 6 API demo
Create a virtual environment, install requirements, and start FastAPI:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

The API provides:
- `GET /api/health`
- `POST /api/drivers`
- `GET /api/drivers/{driver_id}`
- `POST /api/quiz/allocate`
- `POST /api/attempts`
- `GET /api/drivers/{driver_id}/history`
- `GET /api/mis`

The frontend automatically attempts `/api/quiz/allocate` first; if the API is unavailable it falls back to local intelligent allocation and localStorage.

## Production architecture
Use the included `db/schema.sql` to move persistence to PostgreSQL. Recommended production layers are tablet/PWA frontend → HTTPS FastAPI API → PostgreSQL → trainer/admin MIS → Power BI or another reporting layer.

## Question bank
`data/questions.json` contains 107 assessment questions: the supplied 100-question bilingual bank plus 7 Tata Samarth questions from the supplied 147-question deep-read bank. The seven Tata Samarth additions use English as Hindi fallback because a Hindi translation was not present in that source bank.

## Branding assets
- `assets/logo.png` is cropped from the supplied Tata Motors Commercial Vehicles logo image and is displayed at the **top-left on every app screen**.
- `assets/trucks-index.jpg` is cropped from the supplied truck image to remove the event headline while retaining the truck lineup for the Home/Index hero.

## Scope boundary
This package is a ready-to-run application prototype. It does not claim a live deployed cloud database, live Power BI workspace, production authentication/SSO, or live Tata Motors service integration. Those require deployment credentials and enterprise system integration.
