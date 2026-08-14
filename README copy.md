# Smart Agriculture & Farm Management System

## Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger:
`http://127.0.0.1:8000/docs`

## Authentication

1. POST `/auth/register`
2. POST `/auth/login`
3. Copy `access_token`.
4. Click Swagger **Authorize**.
5. Enter the token and authorize.

Default database is SQLite. For PostgreSQL, change `DATABASE_URL` in `app/config.py`, for example:

`postgresql+psycopg2://postgres:password@localhost:5432/smart_agriculture`

and install `psycopg2-binary`.

## Roles

Admin, Farm Manager, Farmer, Field Worker

## Main API groups

- Authentication: `/auth/*`
- Farms/Fields: `/farms/*`
- Crops: `/crops/*`
- Irrigation: `/irrigation`, `/fields/{field_id}/irrigation`
- Treatments: `/crop-treatments`
- Crop Health: `/crop-health`
- Harvest: `/harvests`
- Sales: `/sales`
- Dashboard: `/dashboard`

## Notes

This implementation uses SQLAlchemy ORM, Pydantic validation, JWT authentication, Argon2 password hashing, role-based access control, business-rule checks, pagination/filtering, automatic sale calculation, critical-health alerts, harvest status updates, and global validation/database exception handlers.
