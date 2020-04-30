from django.contrib import admin
from .models import DeliveryAgents, Store, StoreItems, Orders, Customers


@admin.register(DeliveryAgents)
class DeliveryAgentsAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'phone')
    ordering = ['firstName']
    search_fields = ('firstName', 'lastName')


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
        'orderId', 'customer__firstName', 'customer__lastName', 'deliveryAgent__firstName', 'deliveryAgent__lastName'
    ]
    autocomplete_fields = ['deliveryAgent', 'customer']


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'status',)
    ordering = ['firstName']
    search_fields = ['firstName', 'lastName']
