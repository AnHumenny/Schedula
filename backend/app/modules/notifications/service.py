import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notifications.constants import (
    NotificationEvent,
    SUBJECTS,
)
from app.modules.notifications.mailer import Mailer
from app.modules.notifications.templates import render_email
from app.modules.schedule.models import ScheduleItem
from app.modules.users.models import User

logger = logging.getLogger(__name__)


class NotificationService:
    """Service of notification. """

    def __init__(self, session: AsyncSession, mailer: Mailer):
        self.session = session
        self.mailer = mailer


    async def notify_created(self, item: ScheduleItem) -> None:
        await self._send(item, NotificationEvent.SCHEDULE_CREATED)

    async def notify_updated(self, item: ScheduleItem) -> None:
        await self._send(item, NotificationEvent.SCHEDULE_UPDATED)

    async def notify_deleted(self, item: ScheduleItem) -> None:
        await self._send(item, NotificationEvent.SCHEDULE_DELETED)


    async def _recipients(self, item: ScheduleItem) -> list[User]:
        """   """

        group_ids = [g.id for g in item.groups]
        if not group_ids:
            return []

        stmt = select(User).where(
            User.group_id.in_(group_ids),
            User.is_active.is_(True),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def _send(self, item: ScheduleItem, event: NotificationEvent) -> None:
        """  """

        recipients = await self._recipients(item)

        if not recipients:
            logger.info("No recipients for schedule item %s (%s)", item.id, event)
            return

        subject = SUBJECTS[event]
        body = render_email(
            event,
            discipline_name=item.discipline.name if item.discipline else "—",
            teacher_name=item.teacher.fullname if item.teacher else "—",
            room_label=item.room.number if item.room else "—",
            group_names=", ".join(g.name for g in item.groups) or "—",
            start_datetime=item.start_datetime,
            end_datetime=item.end_datetime,
            description=item.description,
        )

        for user in recipients:
            await self.mailer.send(to=user.email, subject=subject, body=body)
