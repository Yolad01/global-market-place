import logging
from enum import Enum
from typing import NamedTuple

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class NotificationType(str, Enum):
    FORGOT_PASSWORD = "FORGOT_PASSWORD"
    ONBOARDING = "ONBOARDING"
    HELP_AND_SUPPORT = "HELP_AND_SUPPORT"
    SUPPORT_REQUEST_ACKNOWLEDGED = "SUPPORT_REQUEST_ACKNOWLEDGED"


class EmailAttribute(NamedTuple):
    template_name: str
    context: Context
    subject: str


DEFAULT_EMAIL_ATTRIBUTES: dict[NotificationType, EmailAttribute] = {
    NotificationType.ONBOARDING: EmailAttribute(
        template_name="email_verification.html",
        context=Context(),
        subject="Email verification",
    ),
    NotificationType.FORGOT_PASSWORD: EmailAttribute(
        template_name="password_reset.html",
        context=Context(),
        subject="Password Reset Requested",
    ),
    NotificationType.HELP_AND_SUPPORT: EmailAttribute(
        template_name="help_and_support.html",
        context=Context(),
        subject="Support/Help Request",
    ),
    NotificationType.SUPPORT_REQUEST_ACKNOWLEDGED: EmailAttribute(
        template_name="support_request_acknowledged.html",
        context=Context(),
        subject="Support Request Received",
    ),
}


def email_sender(from_address, recipients, email_type: NotificationType, **kwargs):
    default_attributes = DEFAULT_EMAIL_ATTRIBUTES.get(email_type)
    assert default_attributes is not None, "invalid email notification type"

    context = default_attributes.context.update(kwargs.get("context", {}))
    email_body = render_to_string(f"emails/{default_attributes.template_name}", context)

    try:
        send_mail(
            subject=default_attributes.subject,
            message=email_body,
            html_message=email_body,
            from_email=from_address,
            recipient_list=recipients,
            fail_silently=not settings.DEBUG,
        )
        return True
    except Exception:
        logger.warning(f"Error occurred while sending email", exc_info=True)
        return False
