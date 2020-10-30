from time import sleep

from celery.decorators import task
from django.core.mail import send_mail
from celery.utils.log import get_task_logger

from task1.settings import EMAIL_HOST_USER

logger = get_task_logger(__name__)


@task(name='order_email')
def order_email(cust_email, message):
    send_mail('Order Placed!', message,EMAIL_HOST_USER, [cust_email],
              fail_silently=False)
