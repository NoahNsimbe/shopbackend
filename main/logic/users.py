from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from main.logic.email import account_creation_email, account_modification_email, account_deletion_email, \
    account_deactivation_email
from main.models import Customers
from main.serializers import CustomersSerializer, UserSerializer
import logging
logger = logging.getLogger(__name__)


def create_user(user=None, customer=None):
    if user is None:
        user = User()

    if customer is None:
        customer = Customers()

    try:
        user.save()
        created_user = User.objects.get_by_natural_key(user.username)
        created_user.set_password(user.password)
        created_user.save()

        customer.username = user
        serializer = CustomersSerializer(data=CustomersSerializer(customer).data)

        if serializer.is_valid():
            serializer.save()

        try:
            customer_group = Group.objects.get(name='Customers')
            customer_group.user_set.add(user)

        except Group.DoesNotExist:

            customer_group, created = Group.objects.get_or_create(name='Customers')

            if created:
                customer_group.user_set.add(user)
                # ct = ContentType.objects.get_for_model(Customers)
                # add = Permission.objects.create(codename='can_add_project',
                #                                        name='Can change Orders',
                #                                        content_type=ct)
                # change = Permission.objects.create(codename='can_add_project',
                #                                        name='Can change Orders',
                #                                        content_type=ct)
                # customer_group.permissions.add(add)

    except IntegrityError:
        return False, {"Error": "User exists"}

    account_creation_email(user)

    user_serializer = UserSerializer(user)
    return True, user_serializer.data


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
    account = User.objects.get_by_natural_key(username)
    serializer = CustomersSerializer(account.customers).data
    serializer.pop("username")

    user = dict()
    user["first_name"] = account.first_name
    user["last_name"] = account.last_name
    user["email"] = account.email
    user["account info"] = serializer

    return user


def update_account(user):
    if user is None:
        user = User()

    serializer = CustomersSerializer(data=user.customers)

    if serializer.is_valid():

        user.save()
        serializer.save()

        # account_modification_email(user)

        return True, serializer.data
    else:
        return False, serializer.errors


def update_info(new_data, user):

    if user is None:
        user = User()

    new_data["username"] = user.pk

    try:
        old_data = Customers.objects.get(username=user.pk)

        serializer = CustomersSerializer(old_data, data=new_data)

    except Customers.DoesNotExist:

        serializer = CustomersSerializer(data=new_data)

    if serializer.is_valid():

        serializer.save()
        serializer.fields.pop("username")

        return True, serializer.data
    else:
        return False, serializer.errors


def deactivate_account(user=None):
    if user is None:
        user = User()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.is_active = False
        updated_user.save()

        account_deactivation_email(updated_user)

        return True, None
    else:
        return False, {"Error": "Invalid data"}


def delete_account(user=None):
    if user is None:
        user = User()

    updated_user = authenticate(username=user.username, password=user.password)

    if updated_user is not None:
        updated_user.is_active = False
        updated_user.save()

        account_deletion_email(updated_user)

        return True, None
    else:
        return False, {"Error":"Invalid data"}
