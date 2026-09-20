# TATA DTM Main Driver Training Application — V40.1

This package hosts the complete Tata Motors Driver Training V40 browser application.

## Included
- index.html — complete driver training application
- main.py — FastAPI static host
- index.py — FastAPI compatibility import
- requirements.txt
- Dockerfile
- render.yaml

## Important
The browser application uses the configured Supabase publishable key and Supabase Anonymous Auth for driver registration and training progress. The publishable key is safe for browser use; never add a service-role/secret key to index.html.

The application now:
- keeps registration details when a save fails;
- displays the actual registration error below the Save button;
- retries once after an expired/invalid 401 session;
- prevents duplicate clicks while registration is being saved;
- explicitly establishes anonymous Auth before driver registration;
- proceeds to Module 1 only after driver and module initialization succeed.

## Render
Build: `pip install -r requirements.txt`
Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
Python: `3.13.5`

No PostgreSQL tables are created or modified by main.py.
