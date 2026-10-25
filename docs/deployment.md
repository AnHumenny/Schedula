# Deployment

## Requirements

The backend is configured for Python 3.13+, PostgreSQL, and the pinned Python dependencies in `requirements.txt`. The database driver is asyncpg. Redis and SMTP are optional integrations.

## Local setup

From the backend directory:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp env_example .env             # then edit the values
```

Set at least `DATABASE_URL` and `SECRET_KEY` in `.env`. `DATABASE_URL` must use an async PostgreSQL URL such as `postgresql+asyncpg://user:password@localhost:5432/schedula`. Keep real secrets out of version control.

Run migrations and start the API:

```bash
alembic upgrade head
uvicorn main:app --reload --port 8007
```

The default local API is `http://127.0.0.1:8007`; health check: `/health`; Swagger UI: `/docs`; ReDoc: `/redoc` when enabled.

## Configuration

| Variable                                                                                                                                                               | Purpose                                                                                                                                                        |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `APP_NAME`, `DEBUG`, `PORT`                                                                                                                                            | Application metadata/debug flag and documented port. Uvicorn's command-line port controls the example launch.                                                  |
| `ENABLE_API_DOCS`                                                                                                                                                      | Enables `/docs`, `/redoc`, and `/openapi.json`.                                                                                                                |
| `DATABASE_URL`                                                                                                                                                         | Required async SQLAlchemy database URL.                                                                                                                        |
| `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`                                                                                                               | JWT settings. Security code currently fixes HS256 and a 60-minute token lifetime; those implementation constants take precedence over the latter two settings. |
| `ALLOWED_ORIGINS`                                                                                                                                                      | Comma-separated origins or JSON array for CORS.                                                                                                                |
| `REDIS_URL`                                                                                                                                                            | Optional Redis storage URL for rate limiting; unset uses in-process storage.                                                                                   |
| `TRUSTED_IPS`, `RATE_LIMIT_ENABLED`, `DEFAULT_RATE_LIMIT`, `RATE_LIMIT_AUTH`, `RATE_LIMIT_READ`, `RATE_LIMIT_WRITE`, `RATE_LIMIT_GROUP_OPERATION`, `RATE_LIMIT_HEALTH` | Rate limiter configuration. `RATE_LIMIT_ENABLED` and `RATE_LIMIT_HEALTH` are declared but endpoint limiting is driven by the configured per-route constants.   |
| `SMTP_ENABLED`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, `SMTP_USE_TLS`                                                                    | Optional email delivery settings.                                                                                                                              |
| `ENV_SCHEDULER_FILE`                                                                                                                                                   | Optional path to the environment file; defaults to `.env`.                                                                                                     |

## Migrations

Alembic obtains the database URL from application settings and imports `app.core.models_registry` to populate metadata. Create a revision after model changes and inspect it before applying:

```bash
alembic revision --autogenerate -m "describe schema change"
alembic upgrade head
```

To inspect the current revision, use `alembic current`; to roll back one revision, use `alembic downgrade -1`. Ensure the database exists and is reachable before running migrations.

## Production notes

Run Uvicorn behind a production ASGI process manager or reverse proxy, configure HTTPS and production CORS origins, use a strong secret, and provision PostgreSQL (plus Redis/SMTP if enabled). The application adds security response headers and supports trusted IP/rate limit settings. The sibling `frontend/` app is built with `npm run build`; serve the resulting Vite `dist/` bundle from a static web server and configure a reverse proxy for `/api` (or set `VITE_API_URL` at build time). No Dockerfile, compose configuration, frontend deployment manifest, or automated production deployment manifest is included in this repository.
