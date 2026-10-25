# Business Logic

## Schedule items

A schedule item represents one lesson with a teacher, discipline, room, start/end datetimes, type, status, optional description, and zero or more groups. A profile audience can also be associated through `schedule_audience` in bulk copy SQL. Create and update operations check room overlap using the interval predicate `existing.start < requested.end AND existing.end > requested.start`. The current implementation does not check teacher or group conflicts. Datetime timezone information is stripped before persistence by the schedule service.

Creating a schedule item resolves every supplied group ID and rejects unknown groups. Updating can replace the group set through `group_ids`. Standard create/update/delete operations attempt to notify active users assigned to the affected groups by email; mail/SQLAlchemy notification exceptions are logged and do not prevent the main operation from completing.

## Copying a schedule

The copy endpoints are administrator-only and take an inclusive-looking pair of dates in the request schema, but SQL selects source rows with a half-open interval: `start_datetime >= source_start` and `start_datetime < source_end`. Thus `source_end` itself is excluded.

1. The caller selects either a group (`group_id`) or an academic direction (`direction_id`), a source date interval, and `weeks_to_copy`.
2. The operation selects all schedule items starting in that interval which are associated with the selected group or with any group in the direction.
3. Each selected item is copied once per generated week number from 1 through `weeks_to_copy`; start and end are shifted by seven days per copy.
4. Teacher, discipline, room, lesson type, status, description are copied. Group links are copied; profile audience links are also copied.
5. New IDs are allocated from `schedule_items_id_seq`. The operation inserts rows and association links directly using PostgreSQL SQL. It does not check for overlapping lessons or pre-existing target records and does not send schedule email notifications.
6. The repository leaves transaction completion to the request session dependency. Exceptions propagate; the dependency rolls back the request transaction.

## Bulk deletion

Deletion by group or direction selects schedule items whose start time falls from midnight on `start_date` through (but excluding) midnight after `weeks_to_delete` weeks. Selected schedule item rows are deleted; association rows rely on the declared cascading foreign keys. The request session commits on success and rolls back on exception. Because deletion is by schedule item, deleting an item shared by multiple groups removes it for all associated groups.

## Authentication and administration

Login accepts a username or email and password, verifies the stored password hash, and rejects inactive accounts. A signed JWT contains the user's ID and role; protected requests resolve the current active user from the token. Administrative endpoints require the `ADMIN` role. Logout is stateless: clients discard the token; the API does not maintain a token revocation list.
