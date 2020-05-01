from main.logic.email import order_change_email, order_creation_email, order_deletion_email
from main.logic.models import OrderClass
from main.models import Orders
from main.serializers import OrdersSerializer


def fetch_orders(customer):
    orders = Orders.objects.filter(customer=customer)
    serializer = OrdersSerializer(orders, many=True).data
    return serializer


def orders_history(customer_id):
    orders = Orders.objects.filter(customerId=customer_id)
    serializer = OrdersSerializer(orders, many=True).data
    return serializer


def place_order(user_order=None):

    if user_order is None:
        user_order = OrderClass()

    serializer = OrdersSerializer(data=user_order)

    if serializer.is_valid():

        serializer.save()

        order_creation_email(user_order)

        return True

    return False


def alter_order(user_order=None):

    if user_order is None:
        user_order = OrderClass()

    if str(user_order.status).upper() == 'PENDING':

        serializer = OrdersSerializer(data=user_order)

        if serializer.is_valid():
            db_orders = Orders.objects.filter(orderId=user_order.orderId)
            db_orders.delete()

            serializer.save()

            order_change_email(user_order)

            return True

    return False


def delete_order(user_order=None):

    if user_order is None:
        user_order = OrderClass()

    if str(user_order.status).upper() == 'PENDING':

        serializer = OrdersSerializer(data=user_order.orderId)
        # serializer.delete()

        order_deletion_email(user_order)

        return True

    return False
