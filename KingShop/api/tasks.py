from celery import shared_task
from main.models import ReturnProduct
from datetime import timezone
from django.conf import settings


@shared_task
def process_return_confirmation():
    unconfirmed_return = ReturnProduct.objects.filter(confirmed=False)
    return unconfirmed_return.update(confirmed=True)


@shared_task
def cancel_returns():
    current_time = timezone.now()
    scheduled_time = getattr(settings, 'CANCEL_RETURNS_TIME', '18:00')
    if current_time.strftime('%H:%M') == scheduled_time:
        ReturnProduct.objects.all().update(confirmed=False)


