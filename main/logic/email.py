import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template import loader, Context
# from main.logic.models import OrderClass
import logging
from shopbackend.settings import BASE_DIR

logger = logging.getLogger(__name__)


def send_email(recipient, subject, message, html_message):

    sender = settings.EMAIL_HOST_USER

    msg = EmailMultiAlternatives(subject, message, sender, [recipient])
    msg.attach_alternative(html_message, "text/html")

    try:
    #    msg.send()
        pass
    except Exception as ex:
        logger.error("Email error")
        logger.error(ex)


def order_change_email(user = None):

    if user is None:
        user = User()

    subject = "NOTIFICATION OF ORDER CHANGE"
    message = None
    path = os.path.join(BASE_DIR + '/templates/', 'email/orders/changed_order.html')

    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
            'order_id': user.orders.order_id,
        }
    )

    send_email(user.email, subject, message, html_message)


def order_creation_email(user):

    if user is None:
        user = User()

    subject = "NOTIFICATION OF ORDER RECIPIENT"
    message = None
    path = os.path.join(BASE_DIR + '/templates/', 'email/orders/received_order.html')

    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
            'order_id': user.orders.order_id,
        }
    )

    send_email(user.email, subject, message, html_message)


def order_deletion_email(user):

    if user is None:
        user = User()

    subject = "NOTIFICATION OF ORDER DELETION"
    message = None
    path = os.path.join(BASE_DIR + '/templates/', 'email/orders/deleted_order.html')

    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
            'order_id': user.orders.order_id,
        }
    )

    send_email(user.email, subject, message, html_message)


def account_creation_email(user):
    if user is None:
        user = User()

    subject = "NOTIFICATION OF ACCOUNT CREATION"
    message = None
    path = os.path.join(BASE_DIR + '/templates/', 'email/accounts/account_creation.html')

    html_message = loader.render_to_string(
        path,
        {
            'first_name': "user.first_name",
        },
    )

    send_email(user.email, subject, message, html_message)


def account_modification_email(user):
    if user is None:
        user = User()

    subject = "NOTIFICATION OF ACCOUNT MODIFICATION"
    message = None
    path = os.path.join(BASE_DIR + '/templates/', 'email/accounts/account_modification.html')

    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
        }
    )

    send_email(user.email, subject, message, html_message)


def account_deletion_email(user):
    if user is None:
        user = User()

    subject = "NOTIFICATION OF ACCOUNT DELETION"
    message = None
    path = os.path.join(BASE_DIR + '/templates/', 'email/accounts/account_deletion.html')

    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
        }
    )

    send_email(user.email, subject, message, html_message)


def account_deactivation_email(user):
    if user is None:
        user = User()

    subject = "NOTIFICATION OF ACCOUNT DELETION"
    message = None
    path = os.path.join(BASE_DIR + '/templates/', 'email/accounts/account_deactivation.html')

    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
        }
    )

    send_email(user.email, subject, message, html_message)
