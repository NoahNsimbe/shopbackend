from random import randint
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader


def create_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # return 'user_{0}/{1}'.format(instance.user.id, filename)
    return '{0}/{1}/{2}'.format(instance.store, instance.category, filename)


def send_email(recipient, subject, message, html_message=None):

    sender = settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, sender, recipient, fail_silently=True, html_message=html_message)
    except Exception:
        pass


def order_update_email(status, order_id, user_name):

    user = User.objects.get_by_natural_key(user_name)

    if status == "DELIVERED":
        subject = "NOTIFICATION OF ORDER DELIVERY"
        message = ""
        path = os.path.join(settings.TEMPLATES, 'email/delivered_order.html')
        html_message = loader.render_to_string(
            path,
            {
                'first_name': user.first_name,
                'order_id': order_id,
            }
        )

        send_email(user.email, subject, message, html_message)

    elif status == "CONFIRMED":
        subject = "ORDER CONFIRMATION"
        message = ""
        path = os.path.join(settings.TEMPLATES, 'email/confirmed_order.html')
        html_message = loader.render_to_string(
            path,
            {
                'first_name': user.first_name,
                'order_id': order_id,
            }
        )

        send_email(user.email, subject, message, html_message)
    else:
        pass


def gen_id(code=None):
    if code is None:
        code = "XXX"
    return '{0}-{1}-{2}'.format(code, randint(10000, 99999), randint(10000, 99999))


def gen_item_id():
    return '{0}-{1}-{2}-{3}'.format("ITEM", randint(1000, 9999), randint(1000, 9999), randint(1000, 9999))


def gen_order_id():
    # date = instance.orderTime
    return '{0}-{1}-{2}-{3}'.format("ORD", randint(1000, 9999), randint(1000, 9999), randint(1000, 9999))


def items_default():
    details = {
        "itemId": [
            {"quantity": "quantity"}
        ]
    }
    return details


def validate_store_id(value):
    value = str(value)
    try:
        comps = value.split("-")
        if not (
                len(comps) == 3 and
                (comps[0] == "ST") and
                comps[1].isdigit() and
                comps[2].isdigit() and
                len(value) == 14):
            raise ValidationError(
                _('%(value)s does not match the required criteria'),
                params={'value': value},
            )
    except Exception:
        raise ValidationError(
            _('%(value)s does not match the required criteria'),
            params={'value': value},
        )


class Agents(models.Model):
    agent_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=30,
        unique=True,
        help_text="Please make sure you begin with the country code, for example : <b><em>+256</em></b>"
    )
    location = models.TextField(blank=True,)

    def __str__(self):
        return "{0}".format(self.agent_id)

    class Meta:
        verbose_name = verbose_name_plural = 'Agents'


class Store(models.Model):
    store_id = models.CharField(
        default=gen_id("ST"),
        validators=[validate_store_id],
        max_length=255,
        primary_key=True,
        help_text="Please use the following format, where X is a number: <b><em>ST-XXXXX-XXXXX</em></b>."
    )
    full_name = models.CharField(
        max_length=255,
        help_text="For example <b><em>Mega Standard Supermarket</em></b>"
    )
    short_name = models.CharField(
        max_length=255,
        help_text="For example <b><em>Mega Standard</em></b>",
        unique=True
    )
    location = models.TextField(blank=True,)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{0}".format(self.short_name)

    class Meta:
        verbose_name = verbose_name_plural = 'Stores'


class StoreItems(models.Model):
    item_id = models.CharField(
        default=gen_item_id,
        unique=True,
        max_length=255,
        help_text="Please use the following format, where X is a number: <b><em>ITEM-XXXX-XXXX-XXXX</em></b>."
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_price = models.FloatField(default=0.00)
    category = models.CharField(default="Not Categorised", max_length=255)
    sub_category = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=create_upload)
    brand = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    key_features = ArrayField(models.CharField(max_length=255), blank=True)
    specifications = ArrayField(models.CharField(max_length=255), blank=True)

    def __str__(self):
        return "{0} : {1}".format(self.store, self.name)

    class Meta:
        verbose_name = verbose_name_plural = 'Items'


class Customers(models.Model):

    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30,
                             help_text="Please make sure you begin with the country "
                                       "code, for example : <b><em>+256</em></b>",
                             )
    location = models.TextField(blank=True,)
    subscription = models.BooleanField(blank=False,)

    def __str__(self):
        return "{}".format(self.customer)

    class Meta:
        verbose_name = verbose_name_plural = 'Customers'
        ordering = ["customer_id"]


class Orders(models.Model):
    DELIVERED = 'DELIVERED'
    NOT_CONFIRMED = 'PENDING'
    CONFIRMED = 'CONFIRMED'

    STATUS_CHOICES = [
        (DELIVERED, 'Delivered'),
        (NOT_CONFIRMED, 'Pending Confirmation'),
        (CONFIRMED, 'Confirmed, awaits delivery'),
    ]

    order_id = models.CharField(default=gen_order_id, primary_key=True, max_length=255)
    customer = models.ForeignKey(User, on_delete=models.CASCADE,)
    address = models.TextField(help_text="Address to deliver the order to",)
    order_time = models.DateTimeField(default=timezone.now,)
    delivery_time = models.DateTimeField(
        blank=True,
        help_text="Date and time the order will be delivered",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_agent = models.ForeignKey(Agents, on_delete=models.CASCADE, blank=True)
    products = ArrayField(JSONField("ItemsInfo", default=items_default))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=NOT_CONFIRMED,)
    send_email = models.BooleanField(default=True,)

    def save(self, *args, **kwargs):

        if self.send_email:
            order_update_email(self.customer, self.order_id, self.status)

        super().save(*args, **kwargs)

    def __str__(self):
        return "{0} : {1}".format(self.customer, self.order_id)

    class Meta:
        verbose_name = verbose_name_plural = 'Orders'
        ordering = ["status", "order_time"]
