-- Tata Motors CV Driver Training V39 -> DTM Production
-- Secure browser architecture: Supabase Anonymous Auth + RLS
-- Run this AFTER enabling Anonymous Sign-Ins in:
-- DTM -> Authentication -> Providers / Sign-in methods -> Anonymous Sign-Ins
--
-- This script does NOT delete workshop/driver data.
-- It removes existing policies on the driver-facing tables and replaces them
-- with policies that restrict an anonymous tablet session to its own driver.

BEGIN;

-- 1) Driver-facing schema compatibility
ALTER TABLE public.drivers
  ADD COLUMN IF NOT EXISTS vehicle_model text;

-- Vehicle Type is no longer collected by V39. Keep the legacy column for
-- compatibility, but it must not block registration.
ALTER TABLE public.drivers
  ALTER COLUMN vehicle_type DROP NOT NULL;

-- 2) Enable RLS
ALTER TABLE public.workshops ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.drivers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.module_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.training_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.final_assessment ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.certificates ENABLE ROW LEVEL SECURITY;

-- 3) Remove old development policies from driver-facing tables.
DO $$
DECLARE r record;
BEGIN
  FOR r IN
    SELECT schemaname, tablename, policyname
    FROM pg_policies
    WHERE schemaname='public'
      AND tablename IN ('workshops','drivers','module_progress','training_sessions','final_assessment','certificates')
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON %I.%I', r.policyname, r.schemaname, r.tablename);
  END LOOP;
END $$;

-- 4) Grants for the authenticated role used by anonymous Supabase Auth users.
GRANT SELECT ON public.workshops TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.drivers TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.module_progress TO authenticated;
GRANT INSERT, SELECT, UPDATE ON public.training_sessions TO authenticated;
GRANT SELECT, INSERT ON public.final_assessment TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.certificates TO authenticated;

-- 5) Workshop master: driver tablets may read active workshops only.
CREATE POLICY v39_workshops_read
ON public.workshops
FOR SELECT TO authenticated
USING (is_active = true);

-- 6) Drivers: an anonymous tablet session can create/read/update only its own row.
CREATE POLICY v39_driver_insert
ON public.drivers
FOR INSERT TO authenticated
WITH CHECK (
  id = (select auth.uid())
  AND COALESCE((select (auth.jwt()->>'is_anonymous')::boolean), false) = true
);

CREATE POLICY v39_driver_select
ON public.drivers
FOR SELECT TO authenticated
USING (
  id = (select auth.uid())
  AND COALESCE((select (auth.jwt()->>'is_anonymous')::boolean), false) = true
);

CREATE POLICY v39_driver_update
ON public.drivers
FOR UPDATE TO authenticated
USING (
  id = (select auth.uid())
  AND COALESCE((select (auth.jwt()->>'is_anonymous')::boolean), false) = true
)
WITH CHECK (
  id = (select auth.uid())
  AND COALESCE((select (auth.jwt()->>'is_anonymous')::boolean), false) = true
);

-- 7) Module progress: only the current driver's rows.
CREATE POLICY v39_module_select
ON public.module_progress
FOR SELECT TO authenticated
USING (driver_id = (select auth.uid()));

CREATE POLICY v39_module_insert
ON public.module_progress
FOR INSERT TO authenticated
WITH CHECK (driver_id = (select auth.uid()));

CREATE POLICY v39_module_update
ON public.module_progress
FOR UPDATE TO authenticated
USING (driver_id = (select auth.uid()))
WITH CHECK (driver_id = (select auth.uid()));

-- 8) Training sessions: driver can create and view only its own sessions.
CREATE POLICY v39_session_insert
ON public.training_sessions
FOR INSERT TO authenticated
WITH CHECK (driver_id = (select auth.uid()));

CREATE POLICY v39_session_select
ON public.training_sessions
FOR SELECT TO authenticated
USING (driver_id = (select auth.uid()));

CREATE POLICY v39_session_update
ON public.training_sessions
FOR UPDATE TO authenticated
USING (driver_id = (select auth.uid()))
WITH CHECK (driver_id = (select auth.uid()));

-- 9) Final assessment: only current driver's attempts.
CREATE POLICY v39_final_select
ON public.final_assessment
FOR SELECT TO authenticated
USING (driver_id = (select auth.uid()));

CREATE POLICY v39_final_insert
ON public.final_assessment
FOR INSERT TO authenticated
WITH CHECK (driver_id = (select auth.uid()));

-- 10) Certificates: only current driver's certificate.
CREATE POLICY v39_certificate_select
ON public.certificates
FOR SELECT TO authenticated
USING (driver_id = (select auth.uid()));

CREATE POLICY v39_certificate_insert
ON public.certificates
FOR INSERT TO authenticated
WITH CHECK (driver_id = (select auth.uid()));

CREATE POLICY v39_certificate_update
ON public.certificates
FOR UPDATE TO authenticated
USING (driver_id = (select auth.uid()))
WITH CHECK (driver_id = (select auth.uid()));

COMMIT;

-- Verification
SELECT 'active_workshops' AS check_name, COUNT(*) AS value
FROM public.workshops WHERE is_active = true
UNION ALL
SELECT 'drivers_rows', COUNT(*) FROM public.drivers
UNION ALL
SELECT 'module_progress_rows', COUNT(*) FROM public.module_progress;
