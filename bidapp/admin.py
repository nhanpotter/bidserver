from django.contrib import admin

from .models import BidItem, User, Shop, BidTransaction

# Register your models here.
admin.site.register(User)
admin.site.register(Shop)
admin.site.register(BidItem)