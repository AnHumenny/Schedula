from datetime import datetime
from app.modules.notifications.constants import NotificationEvent


def _fmt_dt(dt: datetime) -> str:
    """   """
    return dt.strftime("%d.%m.%Y %H:%M")


def render_email(
    event: NotificationEvent,
    *,
    discipline_name: str,
    teacher_name: str,
    room_label: str,
    group_names: str,
    start_datetime: datetime,
    end_datetime: datetime,
    description: str | None = None,
) -> str:
    """Templates for email."""

    header = {
        NotificationEvent.SCHEDULE_CREATED: "У вас новое занятие",
        NotificationEvent.SCHEDULE_UPDATED: "Занятие изменилось",
        NotificationEvent.SCHEDULE_DELETED: "Занятие отменено",
    }[event]

    lines = [
        header,
        "",
        f"Дисциплина: {discipline_name}",
        f"Преподаватель: {teacher_name}",
        f"Аудитория: {room_label}",
        f"Группы: {group_names}",
        f"Время: {_fmt_dt(start_datetime)} — {_fmt_dt(end_datetime)}",
    ]

    if description:
        lines.append(f"Комментарий: {description}")

    lines += ["", "— Schedula"]
    return "\n".join(lines)
