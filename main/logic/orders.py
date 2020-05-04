from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from main.logic.email import order_change_email, order_creation_email, order_deletion_email
from main.models import Orders, gen__id
from main.serializers import OrdersSerializer


def fetch_orders(user):

    if user is None:
        user = User()

    orders = Orders.objects.filter(customer=user.pk)
    serializer = OrdersSerializer(orders, many=True).data
    return serializer


def orders_history(customer_id):
    orders = Orders.objects.filter(customerId=customer_id)
    serializer = OrdersSerializer(orders, many=True).data
    return serializer


def place_order(order, user=None):

    if user is None:
        user = User()

    order["customer"] = user.pk
    order["order_id"] = gen__id("ORD")

    serializer = OrdersSerializer(data=order)

    if serializer.is_valid():

        serializer.save()
        #
        # order_creation_email(user)
        serializer.fields.pop("customer")
        return True, serializer.data

    return False, serializer.errors


def alter_order(new_data, old_data=None, user=None):

    if old_data is None:
        old_data = Orders()

    if user is None:
        user = User()

    new_data["customer"] = user.pk

    if str(old_data.status).upper() == 'PENDING':

        serializer = OrdersSerializer(old_data, data=new_data)

        if serializer.is_valid():

            serializer.save()

            # order_change_email(user)
            serializer.fields.pop("customer")

            return True, serializer.data
        else:
            return False, serializer.errors

    return False, {"Error": "Order already confirmed. Contact us to have your order changed"}


def delete_order(user_order=None):

    if str(user_order.status).upper() == 'PENDING':

        serializer = OrdersSerializer(data=user_order.orderId)
        # serializer.delete()

        order_deletion_email(user_order)

        return True

    return False

# def delete_account(user=None):
#     if user is None:
#         user = User()
#
#     updated_user = authenticate(username=user.username, password=user.password)
#
#     if updated_user is not None:
#         updated_user.is_active = False
#         updated_user.save()
#
#         account_deletion_email(updated_user)
#
#         return True, None
#     else:
#         return False, {"Error":"Invalid data"}
