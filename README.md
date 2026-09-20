# Tata Motors DTM Driver Training — V40.2

Complete Render-ready driver training application with the 99-workshop master.

## Required Render environment variables

- `SUPABASE_URL` = your DTM Supabase project URL
- `SUPABASE_PUBLISHABLE_KEY` = current Supabase **publishable** browser key (`sb_publishable_...`)
- `PYTHON_VERSION` = `3.13.5`

Do NOT put a `service_role` or `sb_secret` key in the browser.

The application injects the two public Supabase configuration values into the HTML at request time. No secret key is stored in the repository.

## Registration flow

Anonymous Supabase Auth is created first. The driver record uses the Auth user UUID as `drivers.id`, consistent with the DTM production RLS design. Module M1–M4 progress is then initialized. The application moves to Module 1 only after successful registration.

The 99-workshop master is embedded in the application and `workshops.csv` is included as a reference copy.
