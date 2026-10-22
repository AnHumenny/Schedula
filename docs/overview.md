# Schedula Backend Overview

Schedula is an academic scheduling backend. It provides an API for maintaining academic directories and publishing class schedules to students and staff.

## Goals and users

The service centralizes timetable data and supports routine schedule maintenance, including copying a recurring week pattern into future weeks and removing schedule entries over a selected period. Its expected users are students and academic staff who view schedules, and administrators who manage reference data and timetable entries.

## Current capabilities

- JWT-based sign-in and current-user lookup.
- User, academic direction, group, profile, teacher, discipline, building, and room management.
- Schedule listing by group, teacher, upcoming time window, or date range.
- Schedule item creation, partial update, and deletion, with room overlap checks.
- Bulk copy and delete operations by group or academic direction.
- Email notifications for schedule item creation, update, and deletion when SMTP is enabled.
- Health endpoint, rate limiting, CORS configuration, and security response headers.

## Technology

Python, FastAPI, Pydantic v2, SQLAlchemy 2 async ORM, PostgreSQL via asyncpg, Alembic, Uvicorn, PyJWT, bcrypt, SlowAPI, and optional SMTP/Redis integrations. See [deployment](deployment.md) for setup and configuration.

The repository includes a React frontend alongside the FastAPI backend. The frontend provides schedule calendars and administrative management screens and consumes the versioned HTTP API. See [Frontend](frontend.md) for routes, client state, and user flows, and [API Reference](api.md) for backend contracts.
