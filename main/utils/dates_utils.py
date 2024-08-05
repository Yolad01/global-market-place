from datetime import datetime

from django.utils import timezone
from django.utils.timezone import make_aware


def datetime_from_string(datetime_string):
    """
    Converts string datetime to python datetime
    """
    if datetime_string:
        try:
            value = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            try:
                value = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S%Z")
            except ValueError:
                return timezone.now()
        return make_aware(value.replace(tzinfo=None), timezone.get_default_timezone())
