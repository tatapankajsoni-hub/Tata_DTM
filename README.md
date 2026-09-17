# Tata Motors CV Driver Training — GitHub Pages Ready

This package is the static, GitHub Pages-ready version of the Driver Training Module Steps 1–6.

## Upload structure

Upload the **contents of this folder**, not the containing folder itself, into the root of your GitHub repository:

- `index.html` must be at repository root
- `css/`
- `js/`
- `assets/`
- `data/`
- `.nojekyll`

## GitHub Pages

1. Create/open your GitHub repository.
2. Upload all files from this folder.
3. Go to **Settings → Pages**.
4. Select **Deploy from a branch**.
5. Branch: `main`.
6. Folder: `/(root)`.
7. Save.
8. Open the URL shown under **Visit site**.

## Important

This version is deliberately static so it works on GitHub Pages without Python, FastAPI, PostgreSQL or another server.

Step 6 includes the Trainer/MIS interface and browser-local persistence. A true central multi-device database/API is a separate production backend and cannot run inside GitHub Pages itself.

## Data persistence

Driver registration, training progress and assessment history use browser `localStorage`. Different tablets/browsers will therefore have separate demo data.
