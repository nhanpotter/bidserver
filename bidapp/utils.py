import datetime
import time
import pytz


def to_unix(python_datetime):
    return int(time.mktime(python_datetime.timetuple()))


def to_python_datetime(unix_timestamp):
    iso_timestamp = datetime.datetime.fromtimestamp(int(unix_timestamp))
    return iso_timestamp.replace(tzinfo=pytz.timezone('Asia/Singapore'))
