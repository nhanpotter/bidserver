import datetime
import time
import pytz


def toUnix(date):
    return int(time.mktime(date.timetuple()))

def toISO(date):
    return datetime.datetime.fromtimestamp(int(date)).replace(tzinfo=pytz.timezone('Asia/Singapore'))