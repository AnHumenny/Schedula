from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.notifications.mailer import Mailer
from app.modules.notifications.service import NotificationService


def get_mailer() -> Mailer:
    """   """
    return Mailer()


async def get_notification_service(
    session: AsyncSession = Depends(get_session),
    mailer: Mailer = Depends(get_mailer),
) -> NotificationService:
    """  """
    return NotificationService(session, mailer)
