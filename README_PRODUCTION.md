## V40.1 hotfix
- Corrected the DTM Supabase publishable key embedded in the static browser build.
- The Supabase RLS SQL must still be executed in the DTM project and Anonymous Sign-Ins must be enabled before driver registration can persist.

# Tata Motors CV Driver Training — V40 Production Web Build

Static, HTTPS-hosting-ready production build of the frozen V39 driver-facing application, connected to the DTM Supabase project.

## Deployment

This is a static web app. Deploy the contents of this folder to Vercel (or another HTTPS static host) with `index.html` as the entry point.

No Node.js build command is required.

## Supabase

The browser uses the Supabase publishable key only. Never place an `sb_secret_...` key in this project.

Before production use in DTM:
1. Enable Anonymous Sign-Ins under Authentication.
2. Run `V40_DTM_AUTH_RLS_SETUP.sql` in the DTM SQL Editor.
3. Confirm `workshops` contains 99 active records.
4. Test registration and confirm rows appear in `drivers` and `module_progress`.

## Driver data flow

Registration -> drivers -> module_progress -> training_sessions -> final_assessment -> certificates

## Session behavior

The active driver/training session is kept in `sessionStorage`, not persistent `localStorage`. A fresh browser tab/session therefore starts at Driver Registration instead of reopening a previous driver's training state.

The central DTM database is not cleared when a browser session ends.
