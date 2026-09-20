# Tata Motors CV Driver Training — FastAPI + PostgreSQL Backend

## Endpoints
- GET `/health`
- GET `/api/workshops`
- POST `/api/drivers/register`
- PATCH `/api/drivers/{driver_id}`
- POST `/api/drivers/{driver_id}/topics`
- POST `/api/drivers/{driver_id}/modules/{module_code}/pretest`
- POST `/api/drivers/{driver_id}/final`
- POST `/api/drivers/{driver_id}/certificate`
- GET `/api/admin/drivers`

## Environment
- `DATABASE_URL`: PostgreSQL connection string
- `DTM_APP_KEY`: public application integration key used by the driver app
- `DTM_ADMIN_KEY`: management API key; never put this in the driver app

The app seeds the supplied 99-workshop CSV on first database startup.
