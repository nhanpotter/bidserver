import datetime

import pytz
from django.conf import settings


def to_unix(python_datetime):
    return int(python_datetime.timestamp())


def to_python_datetime(unix_timestamp):
    """From unix timestamp to python datetime with timezone aware"""
    return datetime.datetime.fromtimestamp(int(unix_timestamp),
                                           pytz.timezone(settings.TIME_ZONE))
