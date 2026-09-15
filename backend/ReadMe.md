

```app/
├── app/
│   ├── core/                  # Core configuration, database, security, and dependencies
│   └── modules/               # Feature-based domain modules
│       ├── auth/              # Authentication and login endpoints
│       ├── directions/        # Academic directions
│       ├── disciplines/       # Study disciplines
│       ├── groups/            # Student groups
│       ├── locations/         # Buildings and rooms infrastructure
│       ├── profiles/          # User profiles
│       ├── schedule/          # Timetable and lesson items
│       ├── teachers/          # Faculty management
│       └── users/             # User accounts and role management

├── .env                       # Environment variables configuration
├── .gitignore                 # Git ignored files configuration
├── alembic.ini                # Alembic migration settings
├── main.py                    # FastAPI application entry point
└── ReadMe.md                  # Project documentation
```

### Schedula
#### — BackendFastAPI + SQLAlchemy 2.0 (async) + Alembic + PostgreSQL + Pydantic v2.

Tech StackPython 3.11+FastAPI — HTTP layer and automatic OpenAPI documentationSQLAlchemy 2.0 (async) — ORM and database operations
Alembic — Database migrationsPostgreSQL — Primary databasePydantic v2 — Data validation and serialization
Uvicorn — ASGI serverpython-jose / passlib — JWT and password hashing
Project Structure
Plaintext.

```
├── app/
│   ├── core/                # Config, sessions, DB, security, dependencies
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── session.py
│   │   ├── security.py
│   │   ├── deps.py
│   │   ├── exceptions.py
│   │   ├── rate_limiter.py
│   │   └── models_registry.py
│   └── modules/             # Domain modules
│       ├── auth/
│       ├── users/
│       ├── profiles/
│       ├── teachers/
│       ├── groups/
│       ├── directions/
│       ├── disciplines/
│       ├── schedule/
│       └── locations/
│           ├── buildings/
│           └── rooms/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── scripts/                 # Utility scripts (seed admin user)
├── alembic.ini
├── main.py
├── .env
├── .gitignore
└── ReadMe.md
Module StructureEach domain module in app/modules/<name>/ follows a uniform layout:Plaintext<module>/
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas (Create/Update/Read)
├── repository.py     # Data access layer (CRUD)
├── service.py        # Business logic
├── router.py         # FastAPI router
├── dependencies.py   # DI providers (repo, service)
└── __init__.py
```

Layers: router → service → repository → models. 
Routers do not interact with the DB directly, services are agnostic of HTTP, and repositories contain no business rules.
The locations module is nested and consists of two submodules — buildings and rooms, each maintaining its own full structure.

**Getting Started.**

```bash
cd backend
```
```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows```
```
Install Dependencies
```Bash
pip install -r requirements.txt ```
```

Configure Environment
Create a .env file in the root directory

Run Migrations
```bash
alembic revision --autogenerate -m "initial"
```
```Bash
`alembic upgrade head
```

Start the Server
```Bash
uvicorn main:app --reload --port 8007
```

API: [http://127.0.0.1:8007](http://127.0.0.1:8007)
Swagger UI: [http://127.0.0.1:8007/docs](http://127.0.0.1:8007/docs)
ReDoc: [http://127.0.0.1:8007/redoc](http://127.0.0.1:8007/redoc)

Apply Migrations
```Bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

```text
All models must be imported inside app/core/models_registry.py, otherwise autogenerate will not detect them.
ScriptsThe scripts/ directory contains helper utilities, including a script to seed an initial test administrator
 account:
 ```
 ```Bash
 python scripts/seed_admin.py
```
```
Development WorkflowAdding a New ModuleCreate app/modules/<name>/ containing models.py, schemas.py, repository.py,
 service.py, router.py, dependencies.py, and __init__.py.Register the model in app/core/models_registry.py.
 Mount the router in main.py (app.include_router(...)).
```

ConventionsLayers: router → service → repository → models.
 - No reverse imports.Pydantic Schemas: Separate Create, Update, and Read schemas per entity; 
 - Read schemas use model_config = ConfigDict(from_attributes=True).
 - Repository: Restricted to CRUD and database queries; contains no business rules.
 - Service: Encapsulates business logic, validations, and cross-service calls via DI.
 - Router: Handles HTTP-specific logic only — receives requests, invokes services, returns schemas.
 - Dependencies: Repository and service providers reside in <module>/dependencies.py.
 - Exceptions: Domain exceptions thrown from app/core/exceptions.py; avoid raising HTTPException directly from service layers.
 - Async: All DB operations use AsyncSession without blocking calls in the event loop.
 - Naming: <Entity>Repository, <Entity>Service, <Entity>Read/Create/Update.
 - Models: Explicit __tablename__, ForeignKey declarations with ondelete, and indexes on foreign keys. 

```
  License  MIT © 2026 Schedula
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.Full license text: https://opensource.org/licenses/MIT
```