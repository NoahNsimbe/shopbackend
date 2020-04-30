from main.models import Store, StoreItems
from main.serializers import StoreSerializer, StoreItemsSerializer


def fetch_stores():
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True).data
    return serializer


def fetch_items(store):
    store_items = StoreItems.objects.filter(store=store)
    serializer = StoreItemsSerializer(store_items, many=True).data
    return serializer
