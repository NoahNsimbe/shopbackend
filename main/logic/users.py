from main.models import Store, StoreItems, Customers
from main.serializers import StoreSerializer, StoreItemsSerializer, CustomersSerializer


def register_user():
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True).data
    return serializer


def fetch_user(user_id):
    details = Customers.objects.filter(customerId=user_id)
    serializer = CustomersSerializer(details, many=True).data
    return serializer


def update_user(store):
    store_items = StoreItems.objects.filter(store=store)
    serializer = StoreItemsSerializer(store_items, many=True).data
    return serializer


def delete_user(store):
    store_items = StoreItems.objects.filter(store=store)
    serializer = StoreItemsSerializer(store_items, many=True).data
    return serializer
