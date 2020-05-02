from django.urls import path
from .views import stores, OrderView, UserView, register, test

urlpatterns = [
    path("stores/", stores, name="stores"),
    path('order/', OrderView.as_view(), name='order'),
    path('user/', UserView.as_view(), name='user'),
    path("register/", register, name="register"),
    path("test/", test, name="test"),
]
