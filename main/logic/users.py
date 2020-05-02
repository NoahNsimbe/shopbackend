from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.db import IntegrityError

from main.logic.email import account_creation_email, account_modification_email, account_deletion_email, \
    account_deactivation_email
# from main.logic.models import UserClass
from main.models import Customers
from main.serializers import CustomersSerializer


def create_user(user=None):
    if user is None:
        user = User()

    try:
        user.save()
        customer_group = Group.objects.get(name='Customers')
        customer_group.user_set.add(user)

    except IntegrityError:

        return False, "User exists"

    account_creation_email(user)

    return True, None


def update_password(user=None):
    if user is None:
        user = User()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.set_password(user.password)
        updated_user.save()

        return True
    else:
        return False


def fetch_user(username):
    details = Customers.objects.filter(customerId=username)
    account = User.objects.get_by_natural_key(username)

    # user = dict()
    #
    # user["email"] = account.email
    # user["username"] = account.username

    serializer = CustomersSerializer(details).data

    return serializer


def update_account(user):
    if user is None:
        user = User()

    serializer = CustomersSerializer(data=user)

    if serializer.is_valid():

        account = User.objects.get_by_natural_key(user.username)
        account.email = user.email

        account.save()
        serializer.save()

        account_modification_email(account)

        return True, None
    else:
        return False, "Missing Data"


def deactivate_account(user=None):
    if user is None:
        user = User()

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
        user = User()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.is_active = False
        updated_user.save()

        account_deletion_email(updated_user)

        return True
    else:
        return False
