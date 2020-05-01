from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from main.logic.models import UserClass
from main.models import StoreItems, Customers
from main.serializers import StoreItemsSerializer, CustomersSerializer


def create_user(user=None):
    if user is None:
        user = UserClass()

    if user.check_registration():

        user.clean()

        registered_user = User.objects.create_user(user.username, user.email, user.password)

        registered_user.is_staff = False
        registered_user.is_superuser = False
        registered_user.first_name = user.first_name
        registered_user.last_name = user.last_name

        registered_user.save()

        return True
    else:
        return False


def update_password(user=None):
    if user is None:
        user = UserClass()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.set_password(user.password)
        updated_user.save()
        return True
    else:
        return False


def fetch_user(user_name):
    details = Customers.objects.filter(customerId=user_name)
    serializer = CustomersSerializer(details, many=True).data
    return serializer


def update_account(store):
    store_items = StoreItems.objects.filter(store=store)
    serializer = StoreItemsSerializer(store_items, many=True).data
    return serializer


def deactivate_account(user=None):
    if user is None:
        user = UserClass()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.is_active = False
        updated_user.save()
        return True
    else:
        return False


def delete_account(user=None):
    if user is None:
        user = UserClass()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.is_active = False
        updated_user.save()
        return True
    else:
        return False
