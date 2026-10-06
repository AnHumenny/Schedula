import logging
from email.message import EmailMessage
import aiosmtplib
from app.core.config import settings

logger = logging.getLogger(__name__)


class Mailer:
    """Sending emails via SMTP. If SMTP_ENABLED=False — just logger."""

    @staticmethod
    async def send(to: str, subject: str, body: str) -> None:
        """   """

        if not settings.SMTP_ENABLED:
            logger.info("[mailer:disabled] to=%s subject=%r", to, subject)
            return

        message = EmailMessage()
        message["From"] = settings.SMTP_FROM
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        try:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                use_tls=settings.SMTP_USE_TLS,
            )
        except (aiosmtplib.SMTPException, OSError):
            logger.exception("Failed to send email to %s", to)
