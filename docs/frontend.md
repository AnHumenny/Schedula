# Frontend

## Purpose and stack

The `frontend/` directory contains the Schedula browser application. It is a React 19 single-page app written in TypeScript and built with Vite. React Router provides client-side navigation, TanStack Query manages server state and mutations, Zustand stores authentication state, Axios calls the backend, and `react-big-calendar` with Moment.js renders timetables. UI styles use CSS modules alongside shared global styles.

## Application structure

- `src/app/` contains the entry point, router, query provider, global layout, and `RequireAuth` route guard.
- `src/pages/` contains route-level screens: dashboard, schedule list/calendars/editor/operations, login, and management pages for students, teachers, groups, directions, disciplines, profiles, and locations.
- `src/components/calendar/` contains the reusable calendar views, event mapping, lookup queries, filters, event modal, toolbar, legend, and statistics.
- `src/features/auth/model/store.ts` contains the persisted Zustand auth store.
- `src/shared/api/` contains the Axios client, typed endpoint functions, and API types.
- `src/shared/components/`, `hooks/`, `types/`, `utils/`, and `styles/` provide reusable UI and domain support.

The code follows an FSD-lite arrangement: route pages compose features and shared code; shared code should remain independent of pages and feature modules. React Query owns remote data and cache invalidation. Local component state handles form values, filters, and modal state.

## Routes and user flows

| Route                                                                                         | Screen                                                 | Current access behavior                                                                                                                                                                                                          |
|-----------------------------------------------------------------------------------------------|--------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/login`                                                                                      | Sign-in                                                | Public. On successful login, stores the JWT, fetches `/auth/me`, then routes admins to `/dashboard` and users to `/schedule/calendar`.                                                                                           |
| `/schedule/calendar`                                                                          | Public calendar page                                   | No frontend role guard. It displays a sign-in button when no token exists. The calendar data queries still call protected backend endpoints, so anonymous data loading currently requires backend/API changes or authentication. |
| `/` and nested admin pages                                                                    | Layout, dashboard, schedule and reference-data screens | Wrapped in `RequireAuth` with `requireRole="ADMIN"`. A user with role `USER` is redirected to `/schedule/calendar`; unauthenticated users go to `/login`.                                                                        |
| `/schedule`                                                                                   | Upcoming schedule                                      | Admin schedule overview with filters and links to the calendar.                                                                                                                                                                  |
| `/schedule/calendar/admin`                                                                    | Admin calendar                                         | Calendar UI with create/edit/delete actions.                                                                                                                                                                                     |
| `/schedule/create`, `/schedule/:id/edit`                                                      | Schedule item forms                                    | Admin-only create and edit flows.                                                                                                                                                                                                |
| `/schedule/operations`                                                                        | Bulk schedule operations                               | Admin form for copy/delete by group or direction.                                                                                                                                                                                |
| `/students`, `/teachers`, `/groups`, `/directions`, `/disciplines`, `/profiles`, `/locations` | Reference/account management                           | Admin-only pages.                                                                                                                                                                                                                |

The route table in `src/app/router.tsx` is authoritative. Some route descriptions in `frontend/README.md` predate the current router and may differ (for example, current calendar paths are `/schedule/calendar` and `/schedule/calendar/admin`).

## Authentication and API calls

The Axios base URL is `VITE_API_URL`, defaulting to `/api/v1`; both checked-in development and production environment files currently set `/api/v1`. The Vite development server runs on port `5174` and proxies `/api` to `http://127.0.0.1:8007`.

A request interceptor reads `token` from `localStorage` and adds `Authorization: Bearer ...`. The persisted Zustand store (storage key `auth`) also holds token and current user. On a `401` outside the configured public paths, the response interceptor clears the store and redirects to `/login`. Login calls `/auth/login`, stores the returned access token, then calls `/auth/me` to resolve role and account details. Logout clears local state; the backend logout endpoint is stateless.

Typed calls are centralized in `src/shared/api/endpoints.ts`; pages should call these wrappers rather than Axios directly. TanStack Query caches reads, retries failed queries once, and mutations invalidate the relevant entity or schedule query keys.

The login page also contains a local development fallback that creates demo ADMIN/USER state after an API login failure. This is client-side navigation state only: its `demo-*` token is not a backend JWT and cannot authorize protected API requests.

## Schedule workflows

The public and admin calendars query the schedule for the visible date range, fetch lookup lists for groups, directions, teachers, disciplines, rooms, and buildings, and map IDs to display labels. The admin calendar supports item creation, editing, and deletion. The operations page lets an administrator choose copy/delete, group/direction target, source or start date, and a week count, then calls the corresponding bulk endpoint and invalidates cached schedule queries.

The frontend's copy form labels a maximum of 52 weeks, but its code only checks that the count is at least one; backend request schemas also declare no upper bound. Actual selection boundaries and copy/delete semantics are described in [Business Logic](business-logic.md).

## Development and build

From `frontend/`:

```bash
npm install
npm run dev
```

Vite serves the app at `http://localhost:5174`. For a production bundle and local preview:

```bash
npm run build
npm run preview
```

`npm run lint` runs ESLint. Configure `VITE_API_URL` for the target API. In production, `/api/v1` requires a same-origin reverse proxy or set `VITE_API_URL` to the backend API base URL. This repository does not include a frontend deployment manifest or reverse proxy configuration.
