from django.apps import AppConfig


class BidappConfig(AppConfig):
    name = 'bidapp'

    def ready(self):
        from .scheduler import start
        start()
