## Schedula
```
Web application for educational institution schedule management: 
students, teachers, groups, academic directions, disciplines, classroom infrastructure, 
and a class schedule calendar with administrative and public views.
What's Inside
backend/ — REST API built with FastAPI + SQLAlchemy 2.0 (async) + Alembic + PostgreSQL.
frontend/ — Single-Page Application (SPA) built with React 18 + TypeScript + Vite + TanStack Query + Zustand.
Each part is self-contained and run separately. Refer to the README inside the respective directory for details.
FeaturesAuthentication — JWT-based, roles (admin/teacher/student), protected routes.
Directories — Users, profiles, teachers, groups, directions, disciplines.
Classroom Infrastructure — Buildings and rooms.
Schedule — Lessons linked to groups, teachers, disciplines, and rooms.
Calendar — Admin view with drag-and-drop and editing, plus a public read-only view with filters.
Dashboard — Summary metrics and quick actions.
Tech Stack (Brief)LayerTechnologiesBackendPython 3.13, FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL, Pydantic v2
FrontendReact 18, TypeScript, Vite, React Router v6, TanStack Query, Zustand, AxiosCalendar
react-big-calendar + momentRepository
```

**Structure**
```
Schedula/
├── backend/
│   ├── app/
│   │   ├── core/         # Config, DB, sessions, security, DI
│   │   └── modules/      # Domain modules (auth, users, groups, schedule, ...)
│   ├── alembic/          # Migrations
│   ├── scripts/          # Seed scripts
│   ├── main.py
│   └── README.md         # Detailed backend documentation
├── frontend/
│   ├── src/
│   │   ├── app/          # Router, providers, guards, Layout
│   │   ├── components/   # Calendar and major components
│   │   ├── pages/        # Route-level pages
│   │   ├── features/     # Features (auth)
│   │   └── shared/       # api, ui, hooks, constants, styles, types, utils
│   ├── vite.config.ts
│   └── README.md         # Detailed frontend documentation
└── README.md             # This file
```

Quick StartFull instructions are available in backend/README.md and frontend/README.md. 
Below is the minimum setup required to run everything locally.

**Backend**

```Bash
cd backend
```

```bash 
python -m venv .venv
```

```bash
source .venv/bin/activate 
```    

```bash
pip install -r requirements.txt
```

**Create a .env file with DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES**

Run Migrations
```bash
alembic revision --autogenerate -m "initial"
```

```bash
alembic upgrade head
```

```bash
python3 scripts/seed_all.py

```
```bash
uvicorn main:app --reload --port 8007
```
```
· API: [http://127.0.0.1:8007](http://127.0.0.1:8007)
· Swagger: [http://127.0.0.1:8007/docs](http://127.0.0.1:8007/docs)
· ReDoc: [http://127.0.0.1:8007/redoc](http://127.0.0.1:8007/redoc)
```

**Frontend**

```Bash
cd frontend
```

```Bash
npm install
```

```Bash
npm run dev
```

```
Application: http://localhost:5174 · proxies /api/* to [http://127.0.0.1:8007](http://127.0.0.1:8007) by default.
Detailed Documentation 
Backend README — Layer architecture, modules, migrations, seeds, conventions.
Frontend README — FSD-lite architecture, routing, data fetching, calendar, styling.
Development WorkflowBranches: main is stable, dev is active work, features are developed in dedicated branches.
Frontend — ESLint + Prettier.
API Contracts: The frontend relies on the OpenAPI spec available at /docs.License
MIT © 2026 Schedula license 
text: LICENSE · https://opensource.org/licenses/MIT
```