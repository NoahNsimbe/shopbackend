import os
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from main.logic.models import OrderClass


def send_email(recipient, subject, message, html_message=None):

    sender = settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, sender, recipient, fail_silently=True, html_message=html_message)
    except Exception:
        pass


def order_update_email(customer, order_id, status):

    recipient = "nsimbenoah@gmail.com"
    try:
        first_name = customer
    except Exception:
        return

    if status == "DELIVERED":
        subject = "NOTIFICATION OF ORDER DELIVERY"
        message = ""
        path = os.path.join(settings.TEMPLATES, 'email/delivered_order.html')
        html_message = loader.render_to_string(
            path,
            {
                'first_name': first_name,
                'order_id': order_id,
            }
        )

        send_email(recipient, subject, message, html_message)

    elif status == "CONFIRMED":
        subject = "ORDER CONFIRMATION"
        message = ""
        path = os.path.join(settings.TEMPLATES, 'email/confirmed_order.html')
        html_message = loader.render_to_string(
            path,
            {
                'first_name': first_name,
                'order_id': order_id,
            }
        )

        send_email(recipient, subject, message, html_message)
    else:
        pass


def order_change_email(user_order):

    if user_order is None:
        user_order = OrderClass()

    recipient = "nsimbenoah@gmail.com"

    subject = "NOTIFICATION OF ORDER RECIPIENT"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/received_order.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': 'first_name',
            'order_id': 'order_id',
        }
    )

    send_email(recipient, subject, message, html_message)


def order_creation_email(user_order):

    if user_order is None:
        user_order = OrderClass()

    recipient = "nsimbenoah@gmail.com"

    subject = "NOTIFICATION OF ORDER RECIPIENT"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/received_order.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': 'first_name',
            'order_id': 'order_id',
        }
    )

    send_email(recipient, subject, message, html_message)


def order_deletion_email(user_order):

    if user_order is None:
        user_order = OrderClass()

    recipient = "nsimbenoah@gmail.com"

    subject = "NOTIFICATION OF ORDER RECIPIENT"
    message = ""
    path = os.path.join(settings.TEMPLATES, 'email/received_order.html')
    html_message = loader.render_to_string(
        path,
        {
            'first_name': 'first_name',
            'order_id': 'order_id',
        }
    )

    send_email(recipient, subject, message, html_message)
