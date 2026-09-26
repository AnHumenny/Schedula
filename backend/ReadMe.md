### Schedula

### Backend

FastAPI + SQLAlchemy 2.0 (async) + Alembic + PostgreSQL + Pydantic v2.

### Tech Stack

- **Python 3.13+**
- **FastAPI** — HTTP layer and automatic OpenAPI documentation
- **SQLAlchemy 2.0 (async)** — ORM and database operations
- **Alembic** — database migrations
- **PostgreSQL** — primary database
- **Pydantic v2** — data validation and serialization
- **Uvicorn** — ASGI server
- **python-jose / passlib** — JWT and password hashing

### Project Structure

```text
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
│       │   └── queries/     # Batch processing SQL queries
│       └── locations/
│           ├── buildings/
│           └── rooms/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── scripts/                 # Utility scripts
├── alembic.ini
├── main.py
├── .env
├── .gitignore
└── ReadMe.md
```


**Module Structure**

Each domain module in app/modules/<name>/ follows a uniform layout:

```text
<module>/
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas (Create/Update/Read)
├── repository.py     # Data access layer (CRUD)
├── service.py        # Business logic
├── router.py         # FastAPI router
├── dependencies.py   # DI providers (repo, service)
└── __init__.py

The application follows the layered architecture:

router → service → repository → models
Routers handle HTTP-specific logic.
Services contain business logic and validation.
Repositories handle database access.
Services are independent of HTTP.
Repositories contain no business rules.

The locations module is nested and consists of two submodules — buildings and rooms — each maintaining its own full structure.
```

**Getting Started**

Create and activate a virtual environment:

```bash
cd backend
```
```bash
python -m venv .venv
```
```bash
source .venv/bin/activate        # Linux/macOS
```
```bash
.venv\Scripts\activate           # Windows
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```
Create a .env file in the project root and configure the required environment variables.

**Database Migrations**

Generate a migration after changing SQLAlchemy models:
```bash
alembic revision --autogenerate -m "migration message"
```
Apply migrations:
```bash
alembic upgrade head
```
All models must be imported in app/core/models_registry.py, otherwise Alembic autogenerate will not detect them.

**Start the Server**
```bash
uvicorn main:app --reload --port 8007
```
```text
API: http://127.0.0.1:8007

Swagger UI: http://127.0.0.1:8007/docs

ReDoc: http://127.0.0.1:8007/redoc
```
**Scripts**

The scripts/ directory contains helper utilities, including a script for creating an initial test administrator account:
```text
python scripts/seed_admin.py
Development Workflow
Adding a New Module
Create app/modules/<name>/.
Add the standard module files:
models.py
schemas.py
repository.py
service.py
router.py
dependencies.py
__init__.py
```
```
Register the module's models in app/core/models_registry.py.
Mount the router in main.py using app.include_router(...).
Conventions
Architecture: router → service → repository → models
Imports: No reverse imports between layers.
Pydantic schemas: Use separate Create, Update, and Read schemas for each entity.
Read schemas: Use model_config = ConfigDict(from_attributes=True).
Repository: Restricted to CRUD operations and database queries; contains no business rules.
Service: Encapsulates business logic, validation, and cross-service calls via dependency injection.
Router: Handles HTTP-specific logic only — receives requests, invokes services, and returns schemas.
Dependencies: Repository and service providers reside in <module>/dependencies.py.
Exceptions: Domain exceptions are defined in app/core/exceptions.py. Avoid raising HTTPException directly from service layers.
Async: All database operations use AsyncSession without blocking calls in the event loop.
Naming: Use <Entity>Repository, <Entity>Service, and <Entity>Read/Create/Update.
Models: Use explicit __tablename__, ForeignKey declarations with ondelete, and indexes on foreign keys.
License
```
MIT © 2026 Schedula

This project is licensed under the MIT License.

See the full license text at https://opensource.org/licenses/MIT.