from django.contrib import admin
from django.contrib.auth.models import User
from .models import Agents, Store, StoreItems, Orders, Customers
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Agents)
class AgentsAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'phone')
    ordering = ['agent_id']
    search_fields = ('User__first_name', 'User__last_name', 'User__username',)
    autocomplete_fields = ('username',)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('short_name',)
    ordering = ['location']
    search_fields = ('short_name', 'full_name',)


@admin.register(StoreItems)
class StoreItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'store')
    ordering = ['store', 'category', 'name']
    search_fields = ('store__short_name', 'store__full_name', 'name', 'brand')
    autocomplete_fields = ['store']


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'customer', 'order_time', 'delivery_time', 'delivery_agent')
    ordering = ['order_time']
    search_fields = [
        'order_id', 'User__first_name', 'User__last_name', 'delivery_agent__firstName', 'delivery_agent__last_name'
    ]
    readonly_fields = ('order_id', 'customer', 'address', 'order_time', 'amount', 'products')
    autocomplete_fields = ['delivery_agent', 'customer']


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'subscription',)
    ordering = ['username']
    search_fields = ['User__username', 'User__first_name', 'User__last_name']
    autocomplete_fields = ['username']
    readonly_fields = ('customer_id', 'username', 'phone', 'location' )


class CustomerInline(admin.StackedInline):
    model = Customers
    can_delete = False
    verbose_name = verbose_name_plural = 'Customer Details'


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
