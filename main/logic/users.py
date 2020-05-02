from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from main.logic.email import account_creation_email, account_modification_email, account_deletion_email, \
    account_deactivation_email
from main.logic.models import UserClass
from main.models import Customers
from main.serializers import CustomersSerializer


def create_user(user=None):
    if user is None:
        user = UserClass()

    registered_user = User.objects.create_user(user.username, user.email, user.password)

    account_creation_email(registered_user)

    return True, None


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
    account = User.objects.get_by_natural_key(user_name)

    user = UserClass()
    user.load(details)
    user.email = account.email
    user.email = account.user_name

    serializer = CustomersSerializer(user).data

    return serializer


def update_account(user):
    if user is None:
        user = UserClass()

    serializer = CustomersSerializer(data=user)

    if serializer.is_valid():

        account = User.objects.get_by_natural_key(user.userName)
        account.email = user.email

        account.save()
        serializer.save()

        account_modification_email(account)

        return True, None
    else:
        return False, "Missing Data"


def deactivate_account(user=None):
    if user is None:
        user = UserClass()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.is_active = False
        updated_user.save()

        account_deactivation_email(updated_user)
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

        account_deletion_email(updated_user)

        return True
    else:
        return False
