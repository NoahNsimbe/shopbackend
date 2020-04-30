from datetime import datetime
from random import randint
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ValidationError
from django.db import models
from main.email.email import send_order_notification


# from django.contrib.auth.models import User
#
#
# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.CharField(max_length=100)


def create_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # return 'user_{0}/{1}'.format(instance.user.id, filename)
    return '{0}/{1}/{2}'.format(instance.store, instance.category, filename)


def gen_id(code=None):
    if code is None:
        code = ""
    return '{0}-{1}-{2}'.format(code, randint(10000, 99999), randint(10000, 99999))


def gen_order_id(instance):
    code = "REF"
    rand_no = randint(10000, 99999)
    date = instance.orderTime
    return '{0}-{1}-{2}'.format(code, rand_no, date)


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
                comps.count == 3 and
                (comps[0] == "ST") and
                comps[1].isdigit() and
                comps[2].isdigit() and
                value.count == 14):
            raise ValidationError(
                _('%(value)s does not match the required criteria'),
                params={'value': value},
            )
    except Exception:
        raise ValidationError(
            _('%(value)s does not match the required criteria'),
            params={'value': value},
        )


class DeliveryAgents(models.Model):
    agentId = models.CharField(default=gen_id("AG"), unique=True, max_length=255)
    firstName = models.CharField(default="", max_length=255)
    lastName = models.CharField(default="", max_length=255)
    phone = models.CharField(default="+2567XXXXXXXX", max_length=13)
    email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return "{0} {1}".format(self.firstName, self.lastName)

    class Meta:
        verbose_name = verbose_name_plural = 'Delivery Agents'


class Store(models.Model):
    storeId = models.CharField(
        default=gen_id("ST"),
        validators=[validate_store_id],
        max_length=255,
        unique=True,
        help_text="Please use the following format, where X is a number: <em>ST-XXXXX-XXXXX</em>.")
    fullName = models.CharField(max_length=255)
    shortName = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{0}".format(self.shortName)

    class Meta:
        verbose_name = verbose_name_plural = 'Stores'


class StoreItems(models.Model):
    itemId = models.CharField(default=gen_id, unique=True, max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unitPrice = models.FloatField(default=0.00)
    category = models.CharField(default="Not Categorised", max_length=255)
    subCategory = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=create_upload, height_field=5, width_field=5)
    brand = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    keyFeatures = ArrayField(models.CharField(max_length=255), blank=True)
    specifications = ArrayField(models.CharField(max_length=255), blank=True)

    def __str__(self):
        return "{0} : {1}".format(self.store, self.name)

    class Meta:
        verbose_name = verbose_name_plural = 'Items'


class Customers(models.Model):
    ACTIVE = 'Active'
    BLOCKED = 'Blocked'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (BLOCKED, 'Blocked')
    ]
    customerId = models.CharField(default=gen_id("CUS"), unique=True, max_length=255)
    firstName = models.CharField(default="", max_length=255,)
    lastName = models.CharField(default="", max_length=255,)
    phone = models.CharField(default="+2567XXXXXXXX", max_length=13,)
    email = models.EmailField(max_length=254, blank=True,)
    location = models.TextField(blank=True,)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ACTIVE,)

    def __str__(self):
        return "{0} {1}".format(self.firstName, self.lastName)

    class Meta:
        verbose_name = verbose_name_plural = 'Customers'
        ordering = ["firstName"]


class Orders(models.Model):
    DELIVERED = 'DELIVERED'
    NOT_CONFIRMED = 'PENDING'
    CONFIRMED = 'CONFIRMED'

    STATUS_CHOICES = [
        (DELIVERED, 'Delivered'),
        (NOT_CONFIRMED, 'Pending Confirmation'),
        (CONFIRMED, 'Confirmed, awaits delivery'),
    ]

    orderId = models.CharField(default=gen_order_id, unique=True, max_length=255)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE,)
    address = models.TextField()
    orderTime = models.DateTimeField(default=datetime.now(),)
    deliveryTime = models.DateTimeField(blank=True,)
    amount = models.FloatField(default=0.00,)
    deliveryAgent = models.ForeignKey(DeliveryAgents, on_delete=models.CASCADE,)
    products = ArrayField(JSONField("ItemsInfo", default=items_default))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=NOT_CONFIRMED,)
    send_email = models.BooleanField(default=True,)

    def save(self, *args, **kwargs):

        if self.send_email:
            send_order_notification(self.customer, self.orderId, self.status)

        super().save(*args, **kwargs)

    def __str__(self):
        return "{0} : {1}".format(self.customer, self.orderId)

    class Meta:
        verbose_name = verbose_name_plural = 'Orders'
        ordering = ["status", "orderTime"]
