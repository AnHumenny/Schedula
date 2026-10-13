from enum import Enum


class NotificationEvent(str, Enum):
    """Sending event."""

    SCHEDULE_CREATED = "schedule_created"
    SCHEDULE_UPDATED = "schedule_updated"
    SCHEDULE_DELETED = "schedule_deleted"


SUBJECTS: dict[NotificationEvent, str] = {
    NotificationEvent.SCHEDULE_CREATED: "Новое занятие в расписании",
    NotificationEvent.SCHEDULE_UPDATED: "Изменение в расписании",
    NotificationEvent.SCHEDULE_DELETED: "Занятие отменено",
}
