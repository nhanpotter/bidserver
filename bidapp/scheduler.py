import random

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.utils import timezone

from .constants import TOKEN_PER_DAY
from .models import BidItem, Notification, User


def scheduler_task():
    """Choose winner, add token to shop and reset user token"""
    # Choose winner for each item and add token to shop
    today = timezone.localtime().date()
    item_qs = BidItem.objects.filter(release_date=today)
    for item in item_qs:
        max_bid_users = item.get_max_bid_users()
        if len(max_bid_users) != 0:
            # Choose winner
            winner = random.choice(max_bid_users)
            item.winner = winner
            item.save()

            # Send notification to winner
            title = "Winner"
            content = item.get_winner_content()
            create_time = int(timezone.now().timestamp())
            Notification.objects.create(user=winner, item=item, title=title,
                                        content=content, create_time=create_time)
            winner.unseen_noti_no = winner.unseen_noti_no + 1
            winner.save()

            # Add token to shop
            shop = item.shop
            shop.accumulate_token = shop.accumulate_token + len(max_bid_users) * item.current_max_bid
            shop.save()

    # Reset user token
    user_qs = User.objects.all()
    for user in user_qs:
        user.token_balance = TOKEN_PER_DAY
        user.save()


def start():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=23, minute=59, timezone=settings.TIME_ZONE)
    scheduler.add_job(scheduler_task, trigger=trigger)
    scheduler.start()
