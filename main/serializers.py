from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Agents, Store, StoreItems, Orders, Customers


class DeliveryAgentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agents
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class StoreItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItems
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):

    # user = UserSerializer(many=False, read_only=True)
    # user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Orders
        fields = '__all__'


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'
