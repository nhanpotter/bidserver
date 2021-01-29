from django.db import models
from django.utils import timezone

from .constants import DEFAULT_TOKEN_THRESHOLD, TOKEN_PER_DAY


# Create your models here.
class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    # attribute
    token = models.PositiveIntegerField(default=TOKEN_PER_DAY)


class Shop(models.Model):
    shop_id = models.CharField(primary_key=True, max_length=50)
    # attribute
    accumulate_token = models.PositiveIntegerField(default=0)


class BidItem(models.Model):
    item_id = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # attribute
    token_threshold = models.PositiveIntegerField(default=DEFAULT_TOKEN_THRESHOLD)
    release_date = models.DateField()
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # item attribute
    name = models.CharField(max_length=255)
    description = models.TextField()
    original_price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    image_url = models.URLField()


class BidTransaction(models.Model):
    item = models.ForeignKey(BidItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # attribute
    token_bid = models.PositiveIntegerField()
    create_time = models.DateTimeField(default=timezone.now)
