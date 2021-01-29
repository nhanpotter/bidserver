import datetime, pytz

from django.test import TestCase
from django.utils import timezone
from .utils import to_unix, to_python_datetime


# Create your tests here.
class UtilsTestCase(TestCase):
    def test_to_unix_utc(self):
        python_datetime_notz = datetime.datetime(2020, 5, 17, 0, 0, 0, 0)
        tz = pytz.timezone('UTC')
        python_datetime = tz.localize(python_datetime_notz)
        unix_timestamp = 1589673600
        self.assertEqual(to_unix(python_datetime), unix_timestamp)

    def test_to_unix_local(self):
        python_datetime_notz = datetime.datetime(2020, 5, 17, 8, 0, 0, 0)
        tz = pytz.timezone('Asia/Singapore')
        python_datetime = tz.localize(python_datetime_notz)
        unix_timestamp = 1589673600
        self.assertEqual(to_unix(python_datetime), unix_timestamp)

    def test_to_unix_django_timezone(self):
        python_datetime_utc = datetime.datetime(2020, 5, 17, 0, 0, 0, 0).replace(tzinfo=pytz.UTC)
        python_datetime = timezone.localtime(python_datetime_utc)
        unix_timestamp = 1589673600
        self.assertEqual(to_unix(python_datetime), unix_timestamp)

    def test_to_python_datetime(self):
        unix_timestamp = 1589673600
        python_datetime_utc = datetime.datetime(2020, 5, 17, 0, 0, 0, 0).replace(tzinfo=pytz.UTC)
        python_datetime = timezone.localtime(python_datetime_utc)
        self.assertEqual(to_python_datetime(unix_timestamp), python_datetime_utc)
        self.assertEqual(to_python_datetime(unix_timestamp), python_datetime)
