from celery import shared_task
from main.models import ReturnProduct
from datetime import datetime, timezone
from pytz import timezone as tz


@shared_task
def process_return_confirmation():
    unconfirmed_return = ReturnProduct.objects.filter(confirmed=False)
    for return_product in unconfirmed_return:
        return_product.confirmed = True
        return_product.save()

    return len(unconfirmed_return)


@shared_task
def cancel_returns():
    kyev_tz = tz('Europe/Kiev')
    current_time = datetime.now(timezone.utc).astimezone(kyev_tz)
    if current_time.hour == 18 and current_time.minute == 0:
        ReturnProduct.objects.all().update(confirmed=False)
