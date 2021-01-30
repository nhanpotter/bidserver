from django.contrib import admin

from .models import BidItem, User, Shop, BidTransaction, Notification

# Register your models here.
admin.site.register(User)
admin.site.register(Shop)
admin.site.register(BidItem)
admin.site.register(BidTransaction)
admin.site.register(Notification)
