# Schedula — Frontend
***
React + TypeScript + Vite + TanStack Query + Zustand.

## Tech Stack
* **React 18** + **TypeScript**
* **Vite** — Build tool and development server
* **React Router v6** — Routing configuration
* **TanStack Query** — Server state management and caching
* **Zustand** — Client state management (auth)
* **Axios** — HTTP client
* **react-big-calendar** + **moment** — Calendar scheduling
* **CSS Modules** — Component-scoped styles

---

## Project Structure

```
src/
├── app/                      # Application entry, layout, routing, guards, and providers
│   ├── guards/               # Route security and authentication guards
│   ├── providers/            # React context and query providers
│   ├── App.tsx               # Root component
│   ├── Layout.tsx            # Main layout wrapper
│   ├── Layout.css            # Layout styles
│   ├── main.tsx              # Application entry point
│   └── router.tsx            # Application routing configuration
├── assets/                   # Static assets (images, icons, SVGs)
├── components/               # Feature-agnostic complex components
│   └── calendar/             # Calendar views, UI elements, hooks, and utilities
├── features/                 # Feature-specific modules and state
│   └── auth/                 # Authentication state and store
├── pages/                    # Page-level components
│   ├── DashboardPage/        # Dashboard view
│   ├── DirectionsPage/       # Academic directions management page
│   ├── DisciplinesPage/      # Disciplines management page
│   ├── GroupsPage/           # Student groups management page
│   ├── LocationsPage/        # Buildings and rooms management page
│   ├── LoginPage/            # Login page and styles
│   ├── ProfilesPage/         # User profiles page
│   ├── Schedule/             # Schedule, timetable views, and admin/public calendars
│   ├── StudentsPage/         # Students management page
│   └── TeachersPage/         # Teachers management page
└── shared/                   # Shared UI, API clients, types, hooks, utils, and styles
    ├── api/                  # API client configuration, endpoints, and requests
    ├── components/           # Reusable UI components (Button, Input, Modal, Table, etc.)
    ├── constants/            # Application constants
    ├── hooks/                # Custom React hooks (e.g., useCrudModal, useDebounce)
    ├── styles/               # Global CSS files, design tokens, and themes
    ├── types/                # TypeScript type definitions for entities and models
    └── utils/                # Helper utility functions (date formatting, colors, etc.)
```


# Schedula — Frontend

React + TypeScript + Vite + TanStack Query + Zustand.

## Tech Stack

- **React 18** + **TypeScript**
- **Vite** — Build tool and development server
- **React Router v6** — Routing configuration
- **TanStack Query** — Server state management and caching
- **Zustand** — Client state management (auth)
- **Axios** — HTTP client
- **react-big-calendar** + **moment** — Calendar scheduling
- **CSS Modules** — Component-scoped styles

---

## Project Structure

```text

src/
├── app/                      # Application entry, layout, routing, guards, and providers
│   ├── guards/               # Route security and authentication guards
│   ├── providers/            # React context and query providers
│   ├── App.tsx               # Root component
│   ├── Layout.tsx            # Main layout wrapper
│   ├── Layout.css            # Layout styles
│   ├── main.tsx              # Application entry point
│   └── router.tsx            # Application routing configuration
├── assets/                   # Static assets (images, icons, SVGs)
├── components/               # Feature-agnostic complex components
│   └── calendar/             # Calendar views, UI elements, hooks, and utilities
├── features/                 # Feature-specific modules and state
│   └── auth/                 # Authentication state and store
├── pages/                    # Page-level components
│   ├── DashboardPage/        # Dashboard view
│   ├── DirectionsPage/       # Academic directions management page
│   ├── DisciplinesPage/      # Disciplines management page
│   ├── GroupsPage/           # Student groups management page
│   ├── LocationsPage/        # Buildings and rooms management page
│   ├── LoginPage/            # Login page and styles
│   ├── ProfilesPage/         # User profiles page
│   ├── Schedule/             # Schedule, timetable views, and admin/public calendars
│   ├── StudentsPage/         # Students management page
│   └── TeachersPage/         # Teachers management page
└── shared/                   # Shared UI, API clients, types, hooks, utils, and styles
    ├── api/                  # API client configuration, endpoints, and requests
    ├── components/           # Reusable UI components (Button, Input, Modal, Table, etc.)
    ├── constants/            # Application constants
    ├── hooks/                # Custom React hooks (e.g., useCrudModal, useDebounce)
    ├── styles/               # Global CSS files, design tokens, and themes
    ├── types/                # TypeScript type definitions for entities and models
    └── utils/                # Helper utility functions (date formatting, colors, etc.)
```

Architecture Style: FSD-lite — pages are autonomous, and common utilities reside in shared/.

Getting Started
```bash
npm install
````
```bash
npm run dev
```

Application runs at http://localhost:5174.  

By default, frontend requests target /api/*, which Vite proxies to http://127.0.0.1:8007.  
Proxy rules can be configured in vite.config.ts.

Environment Variables
Variable	Description
VITE_API_URL	Base API URL. Defaults to /api (Vite proxy) if omitted.
For production deployments, configure .env.production with a direct backend URL.

Build & Preview

```bash
npm run build       # Build bundle into dist/
npm run preview     # Preview production build locally
```

### Architecture & Layers
```text
app/ — Entry point, providers, router, route guards, and global layout wrapper.
pages/ — One directory per route. Each page is self-contained with its own markup, queries, and local state.
features/ — Reusable business logic features (currently houses auth with Zustand store).
shared/ — Domain-agnostic foundation layer:
api/ — Axios client wrapper, endpoints, and request types.
components/ — UI primitives (Button, Input, Select, Modal, Table, FormModal, PageHeader, CheckboxGroup).
hooks/ — Shared custom hooks (useCrudModal, useDebounce).
constants/ — Calendar and global application constants.
styles/ — Design tokens, global rules, and calendar overrides.
types/ — Domain TypeScript definitions (user, group, direction, discipline, teacher, profile, schedule, location, auth, common).
utils/ — Date helpers, color utilities, and calendar helper functions.
```

Import Rule: pages → features → shared. The components/ (calendar) module stands as an independent layer utilizing only shared/.

Routing
Routes are managed in app/router.tsx. Private routes are wrapped with RequireAuth (app/guards/RequireAuth.tsx), which reads tokens from features/auth/model/store.ts.

Path	Page Component	Access Level
- /login	LoginPage	Public
- /	DashboardPage	Private
- /students	StudentsPage	Private
- /teachers	TeachersPage	Private
- /groups	GroupsPage	Private
- /directions	DirectionsPage	Private
- /disciplines	DisciplinesPage	Private
- /locations	LocationsPage	Private
- /profiles	ProfilesPage	Private
- /schedule	SchedulePage	Private
- /schedule/calendar	ScheduleCalendarAdminPage	Private
- /schedule/public	ScheduleCalendarPublicPage	Public
- /schedule/create	ScheduleItemCreatePage	Private
- /schedule/:id/edit	ScheduleItemEditPage	Private

**Data & State Management**

```TanStack Query — Handles all server data: lists, item details, and mutations. Query keys are structured by entity name (['groups', filters], ['schedule', range], etc.). Mutations automatically trigger invalidateQueries on affected keys.
Zustand — Manages client-side state, primarily authentication (token, user, login/logout). Persisted to localStorage.
Local useState — Controls form values, modals, filter parameters, and temporary UI states.
```

**API Client**
```shared/api/client.ts — Axios wrapper featuring:
Base URL resolution via VITE_API_URL (fallback to /api).
Request interceptor injecting Authorization: Bearer <token> from the auth store.
Response interceptor handling 401 errors by clearing state and redirecting to /login.
shared/api/endpoints.ts — Domain-typed functions consumed by page query hooks.
```

**UI Primitives**
```
All base components reside in shared/components/, each containing a dedicated folder with .tsx and .module.css files, exported centrally via shared/components/index.ts.
Button — Variants (primary, secondary, danger, ghost), sizes, and loading state support.
Input, Select — Controlled fields with label and error states.
Modal — Portal-based modal with Esc key and backdrop click dismissal.
FormModal — Combined modal and form wrapper with unified submit/cancel actions.
Table — Typed list display supporting custom columns and empty states.
PageHeader — Page title bar with primary action triggers (e.g., "Create" buttons).
CheckboxGroup — Checkbox group wrapper for multi-selection scenarios.
```

**Custom Hooks**
useCrudModal — Handles open/close state for create/edit modals and tracks the selected entity.
useDebounce — Debounces values for search inputs and filters.

**Calendar Module**
```
Located in components/calendar/, built on top of react-big-calendar:
CalendarView.tsx — Wrapper handling localization (Moment.js, Russian locale) and calendar styles.
ScheduleCalendarAdmin.tsx — Admin view with drag-and-drop, inline editing, and form routing.
ScheduleCalendarPublic.tsx — Public read-only view with filters by direction, group, or teacher.
hooks/ — useCalendarEvents (fetches range-based events) and useCalendarLookups (lookup data for filters).
ui/ — Subcomponents: CustomToolbar, CustomDayHeader, EventComponent, EventDetailsModal, CalendarFilters, CalendarLegend, CalendarStats.
lib/constants.ts — Mappings for colors, locales, and views.
Helpers — shared/utils/calendar.ts, shared/utils/date.ts, shared/utils/colors.ts.
```

**Styling**
```
shared/styles/tokens.css — CSS variables for colors, spacings, radiuses, and typography.
shared/styles/global.css — CSS reset and base rules.
shared/styles/calendar.css — Style overrides for react-big-calendar.
```

Component styles are isolated in modular CSS files adjacent to components.
Development Workflow
Adding a New Entity Page
Define types in shared/types/<entity>.ts and export them from shared/types/index.ts.
Implement API functions in shared/api/endpoints.ts.
Create the pages/<Entity>Page/ directory containing <Entity>Page.tsx.
Add navigation links in app/Layout.tsx and routes in app/router.tsx.

Execute queries and mutations directly in the page using useQuery / useMutation, pairing forms with FormModal and useCrudModal.

**Useful Scripts**
```bash
npm run dev       # Start development server with HMR
npm run build     # Generate production bundle
npm run preview   # Preview production build
npm run lint      # Run ESLint checks
```

**Conventions**
Types: Explicitly defined via type or interface inside shared/types/. No raw API responses in components.
Network Calls: Strictly restricted to shared/api.
Server State: Handled exclusively via TanStack Query without manual useEffect and fetch calls.
Client State: Confined to Zustand, restricted to cross-page persistent data.
Isolation: Shared components must remain domain-agnostic and avoid importing from pages/ or features/.
Query Key Conventions: Format as ['<entity>'],['<entity>', id], or ['<entity>', 'list', filters].

License
MIT © 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

Full license text: https://opensource.org/licenses/MIT