# API Reference

All application routes use the `/api/v1` prefix. The health check is `/health`. Interactive API docs are available at `/docs` and `/redoc` when `ENABLE_API_DOCS=true`.

Protected routes require `Authorization: Bearer <access_token>`. Reads generally require an authenticated user; administrative writes require role `ADMIN`. Successful collection/read operations return JSON matching their Pydantic response schemas. Creates normally return `201`; deletes return `204` with no body. Invalid request schemas return FastAPI validation errors; authentication/authorization failures return `401`/`403`. Rate limits can result in `429`.

## Authentication

| Method and path     | Access           | Request / response                                                                   |
|---------------------|------------------|--------------------------------------------------------------------------------------|
| `POST /auth/login`  | Public           | JSON `username` or `email`, and `password`; returns `access_token` and `token_type`. |
| `GET /auth/me`      | Authenticated    | Returns the current user.                                                            |
| `POST /auth/logout` | Public/stateless | Returns `204`; the client discards its token.                                        |

## Core endpoints

| Method and path                                                                                   | Access        | Purpose / key parameters                                                           |
|---------------------------------------------------------------------------------------------------|---------------|------------------------------------------------------------------------------------|
| `GET /users/`, `GET /users/{user_id}`                                                             | Admin         | List (`limit`, `offset`) or get accounts.                                          |
| `POST /users/`, `PATCH /users/{user_id}`, `DELETE /users/{user_id}`                               | Admin         | Manage accounts; create returns `201`, delete `204`.                               |
| `GET /directions/`, `GET /directions/{direction_id}`                                              | Authenticated | List (`limit`, `offset`, `only_active`) or retrieve directions.                    |
| `POST /directions/`, `PATCH /directions/{direction_id}`, `DELETE /directions/{direction_id}`      | Admin         | Manage directions.                                                                 |
| `GET /groups/`, `GET /groups/{group_id}`                                                          | Authenticated | List (`limit`, `offset`, `only_active`) or retrieve groups.                        |
| `GET /groups/by-direction/{direction_id}`                                                         | Authenticated | List groups by direction (`limit`, `offset`).                                      |
| `GET /groups/by-user/{user_id}`                                                                   | Authenticated | Find a user's group.                                                               |
| `POST /groups/`, `PATCH /groups/{group_id}`, `DELETE /groups/{group_id}`                          | Admin         | Manage groups.                                                                     |
| `GET /profiles/`, `GET /profiles/{profile_id}`                                                    | Authenticated | List (`limit`, `offset`, `only_active`) or retrieve profiles.                      |
| `POST /profiles/`, `PATCH /profiles/{profile_id}`, `DELETE /profiles/{profile_id}`                | Admin         | Manage profiles.                                                                   |
| `GET /teachers/`, `GET /teachers/{teacher_id}`                                                    | Authenticated | List (`limit`, `offset`, `only_active`) or retrieve teachers.                      |
| `GET /teachers/by-discipline/{discipline_id}`                                                     | Authenticated | Find teachers for a discipline.                                                    |
| `POST /teachers/`, `PATCH /teachers/{teacher_id}`, `DELETE /teachers/{teacher_id}`                | Admin         | Manage teachers.                                                                   |
| `GET /disciplines/`, `GET /disciplines/{discipline_id}`                                           | Authenticated | List (`limit`, `offset`, `only_active`) or retrieve disciplines.                   |
| `GET /disciplines/by-teacher/{teacher_id}`                                                        | Authenticated | Find a teacher's disciplines.                                                      |
| `POST /disciplines/`, `PATCH /disciplines/{discipline_id}`, `DELETE /disciplines/{discipline_id}` | Admin         | Manage disciplines.                                                                |
| `GET /buildings/`, `GET /buildings/{building_id}`                                                 | Authenticated | List (`limit`, `offset`, `only_active`) or retrieve buildings.                     |
| `POST /buildings/`, `PATCH /buildings/{building_id}`, `DELETE /buildings/{building_id}`           | Admin         | Manage buildings.                                                                  |
| `GET /rooms/`, `GET /rooms/{room_id}`                                                             | Authenticated | List (`limit`, `offset`, `only_active`, optional `building_id`) or retrieve rooms. |
| `GET /rooms/by-building/{building_id}`                                                            | Authenticated | List rooms in a building.                                                          |
| `POST /rooms/`, `PATCH /rooms/{room_id}`, `DELETE /rooms/{room_id}`                               | Admin         | Manage rooms.                                                                      |

## Schedule

| Method and path                                                              | Access        | Parameters / purpose                                                                                                                                                                                                    |
|------------------------------------------------------------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `GET /schedule/`                                                             | Authenticated | Paginated list (`limit` 1–200, `offset`).                                                                                                                                                                               |
| `GET /schedule/{item_id}`                                                    | Authenticated | Get one schedule item.                                                                                                                                                                                                  |
| `GET /schedule/group/{group_id}`                                             | Authenticated | Group timetable (`limit`, `offset`).                                                                                                                                                                                    |
| `GET /schedule/teacher/{teacher_id}`                                         | Authenticated | Teacher timetable (`limit`, `offset`).                                                                                                                                                                                  |
| `GET /schedule/upcoming`                                                     | Authenticated | `days` 1–30 (default 7), optional `group_id`/`teacher_id`, `limit` 1–500 (default 200).                                                                                                                                 |
| `GET /schedule/range`                                                        | Authenticated | Required ISO 8601 `start` and `end`; returns entries whose start is in the half-open range.                                                                                                                             |
| `POST /schedule/`, `PATCH /schedule/{item_id}`, `DELETE /schedule/{item_id}` | Admin         | Create/update/delete lesson. Create body contains `group_ids`, `teacher_id`, `discipline_id`, `room_id`, `start_datetime`, `end_datetime`, optional `lesson_type`, `status`, `description`; update fields are optional. |
| `POST /schedule/copy/group`                                                  | Admin         | Body: `source_start`, `source_end`, `weeks_to_copy`, `group_id`.                                                                                                                                                        |
| `POST /schedule/copy/copy_by_direction`                                      | Admin         | Body: `source_start`, `source_end`, `weeks_to_copy`, `direction_id`.                                                                                                                                                    |
| `POST /schedule/delete/group`                                                | Admin         | Body: `start_date`, `weeks_to_delete`, `group_id`.                                                                                                                                                                      |
| `POST /schedule/delete/direction`                                            | Admin         | Body: `start_date`, `weeks_to_delete`, `direction_id`.                                                                                                                                                                  |

Schedule enums use uppercase values from `LessonType` and `LessonStatus` in the database model. Copy and bulk delete endpoints currently return no declared response body. Refer to the schemas in `app/modules/*/schemas.py` for complete field definitions.
