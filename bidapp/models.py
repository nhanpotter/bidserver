from django.db import models
from django.utils import timezone

from .constants import DEFAULT_TOKEN_THRESHOLD, TOKEN_PER_DAY


# Create your models here.
class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    # attribute
    token_balance = models.PositiveIntegerField(default=TOKEN_PER_DAY)


class Shop(models.Model):
    shop_id = models.BigIntegerField(primary_key=True)
    # attribute
    accumulate_token = models.PositiveIntegerField(default=0)


class BidItem(models.Model):
    item_id = models.AutoField(primary_key=True)
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

    @property
    def current_max_bid(self):
        transaction_qs = BidTransaction.objects.filter(item=self).order_by('create_time')
        if len(transaction_qs) == 0:
            return 0

        last_transaction = transaction_qs.last()
        return last_transaction.token_bid

    def get_max_bid_users(self):
        transaction_qs = BidTransaction.objects.filter(item=self)
        ordered_transaction_qs = transaction_qs.order_by('create_time')
        if len(transaction_qs) == 0:
            return []

        current_max_bid = ordered_transaction_qs.last().token_bid
        max_bid_transaction_qs = transaction_qs.filter(token_bid=current_max_bid)
        return [trans.user for trans in max_bid_transaction_qs]


class BidTransaction(models.Model):
    item = models.ForeignKey(BidItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # attribute
    token_bid = models.PositiveIntegerField()
    create_time = models.PositiveBigIntegerField()
