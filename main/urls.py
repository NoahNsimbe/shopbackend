from django.urls import path
from .views import stores, order, register_customer, update_customer, delete_customer, fetch_customer

urlpatterns = [
    path("stores/", stores, name="stores"),
    path("order/", order, name="order"),
    path("register_user/", register_customer, name="register_customer"),
    path("update_user/", update_customer, name="update_customer"),
    path("delete_user/", delete_customer, name="delete_customer"),
    path("fetch_user/", fetch_customer, name="fetch_customer"),
]