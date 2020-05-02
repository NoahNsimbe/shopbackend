from django.contrib import admin
from .models import Agents, Store, StoreItems, Orders, Customers


@admin.register(Agents)
class DeliveryAgentsAdmin(admin.ModelAdmin):
    list_display = ('agentId', 'phone')
    ordering = ['agentId']
    search_fields = ('User__first_name', 'User__last_name', 'User__user_name')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('shortName',)
    ordering = ['location']
    search_fields = ('shortName', 'fullName',)


@admin.register(StoreItems)
class StoreItemsAdmin(admin.ModelAdmin):
    list_display = ('store', 'category', 'name')
    ordering = ['store']
    search_fields = ('store__shortName', 'store__fullName', 'name', 'brand')
    autocomplete_fields = ['store']


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'status', 'customer', 'orderTime', 'deliveryTime', 'deliveryAgent')
    ordering = ['orderTime']
    search_fields = [
        'orderId', 'User__first_name', 'User__last_name', 'deliveryAgent__firstName', 'deliveryAgent__lastName'
    ]
    autocomplete_fields = ['deliveryAgent', 'customer']


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('userName', 'phone', 'subscription',)
    ordering = ['userName']
    search_fields = ['User__userName']
