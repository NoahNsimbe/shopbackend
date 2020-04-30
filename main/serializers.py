from rest_framework import serializers
from .models import DeliveryAgents, Store, StoreItems, Orders, Customers


class DeliveryAgentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAgents
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItems
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'
