from main.logic.email import order_change_email, order_creation_email, order_deletion_email
# from main.logic.models import OrderClass
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


def place_order(order):

    serializer = OrdersSerializer(data=order)

    if serializer.is_valid():

        serializer.save()

        order_creation_email(order)

        return True, None

    return False, "Data not valid"


def alter_order(new_data, old_data=None):

    if old_data is None:
        old_data = Orders()

    if str(old_data.status).upper() == 'PENDING':

        serializer = OrdersSerializer(old_data, data=new_data)

        if serializer.is_valid():

            serializer.save()

            order_change_email(serializer.data)

            return True, None
        else:
            return False, "Invalid data"

    return False, "Order already confirmed. Contact us to have your order changed"


def delete_order(user_order=None):

    if str(user_order.status).upper() == 'PENDING':

        serializer = OrdersSerializer(data=user_order.orderId)
        # serializer.delete()

        order_deletion_email(user_order)

        return True

    return False
