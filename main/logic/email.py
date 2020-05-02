import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader
from main.logic.models import OrderClass


def send_email(recipient, subject, message, html_message=None):

    sender = settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, sender, recipient, fail_silently=True, html_message=html_message)
    except Exception:
        pass


def order_change_email(user_order):

    if user_order is None:
        user_order = OrderClass()

    user = User.objects.get_by_natural_key(user_order.customer)

    subject = "NOTIFICATION OF ORDER RECIPIENT"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/received_order.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
            'order_id': user_order.orderId,
        }
    )

    send_email(user.email, subject, message, html_message)


def order_creation_email(user_order):

    if user_order is None:
        user_order = OrderClass()

    user = User.objects.get_by_natural_key(user_order.customer)

    subject = "NOTIFICATION OF ORDER RECIPIENT"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/received_order.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
            'order_id': user_order.orderId,
        }
    )

    send_email(user.email, subject, message, html_message)


def order_deletion_email(user_order):

    if user_order is None:
        user_order = OrderClass()

    user = User.objects.get_by_natural_key(user_order.customer)

    subject = "NOTIFICATION OF ORDER RECIPIENT"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/received_order.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
            'order_id': user_order.orderId,
        }
    )

    send_email(user.email, subject, message, html_message)


def account_creation_email(user):
    if user is None:
        user = User()

    subject = "NOTIFICATION OF ACCOUNT CREATION"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/account_creation.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
        }
    )

    send_email(user.email, subject, message, html_message)


def account_modification_email(user):
    if user is None:
        user = User()

    subject = "NOTIFICATION OF ACCOUNT MODIFICATION"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/account_modification.html')
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
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/account_deletion.html')
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
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/account_deactivation.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': user.first_name,
        }
    )

    send_email(user.email, subject, message, html_message)
