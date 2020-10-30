from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from django.core.mail import send_mail
from login.settings import EMAIL_HOST_USER

logger = get_task_logger(__name__)

@task(name='order_email')

def order_email(cust_email):
    send_mail('Order Placed!','Order was placed by your account',EMAIL_HOST_USER,[cust_email],
    fail_silently= False)  
    return('email sent!')

@task(name='my_first_task')
def my_first_task(duration):
    sleep(duration)
    send_mail(
        'Order Placed!',
        'Order was placed by your account',
        EMAIL_HOST_USER,
        [EMAIL_HOST_USER],
        fail_silently= False
        )
    return('email sent!')