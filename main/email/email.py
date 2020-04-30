import os
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader


def send_email(recipient, subject, message, html_message=None):

    sender = settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, sender, recipient, fail_silently=True, html_message=html_message)
    except Exception:
        pass


def send_order_notification(customer, order_id, status):

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

    else:
        subject = "NOTIFICATION OF ORDER RECIPIENT"
        message = ""
        path = os.path.join(settings.TEMPLATES, 'email/received_order.html')
        html_message = loader.render_to_string(
            path,
            {
                'first_name': first_name,
                'order_id': order_id,
            }
        )

    send_email(recipient, subject, message, html_message)
