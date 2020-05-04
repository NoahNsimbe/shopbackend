from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from .logic.models import UserClass, OrderClass
from .logic.orders import fetch_orders, place_order, delete_order, alter_order
from .logic.stores import fetch_stores, fetch_items
import json
import logging
from .logic.users import create_user, update_account, fetch_user, update_info, delete_account, deactivate_account
from .models import Orders, Customers, gen__id

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def test(request):
    data = JSONParser().parse(request)
    data["gg"] = "gg"

    return Response(data)


@api_view(['GET', 'POST'])
def stores(request):

    if request.method == 'POST':
        store = request.data.get("store")

        if not store:
            return Response({"Message": "Specify the store"}, status.HTTP_400_BAD_REQUEST)

        data = fetch_items(str(store))
    else:
        data = fetch_stores()

    data = json.dumps(data)

    return Response(data)


# @csrf_exempt
@api_view(['POST'])
def register(request):

    data = JSONParser().parse(request)
    user = User()

    try:
        user.username = data["username"]
        user.email = data["email"]
        user.password = data["password"]

    except KeyError:
        return Response({"Error": "Missing Data"}, status.HTTP_400_BAD_REQUEST)

    success, response = create_user(user)

    if success:
        return Response(response, status.HTTP_201_CREATED)

    return Response(response, status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = fetch_user(str(request.user))
        return Response(data)

    def put(self, request):

        data = JSONParser().parse(request)
        user = User.objects.get_by_natural_key(request.user)

        success, message = update_info(data, user)

        if success:
            return Response(message)
        else:
            return Response(message, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        data = JSONParser().parse(request)
        user = User()

        try:
            user.username = str(request.user)
            user.password = str(data["password"])

        except KeyError:
            return Response({"Error": "Missing Data"}, status.HTTP_400_BAD_REQUEST)

        success, message = deactivate_account(user)

        if success:
            return Response(message, status.HTTP_204_NO_CONTENT)
        else:
            return Response(message, status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get_by_natural_key(request.user)
        data = fetch_orders(user)
        return Response(data)

    def post(self, request):

        data = JSONParser().parse(request)

        user = User.objects.get_by_natural_key(request.user)

        success, response = place_order(data, user)

        if success:
            return Response(response, status.HTTP_201_CREATED)
        else:
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        data = JSONParser().parse(request)
        data["username"] = str(request.user)

        if delete_order(data):
            return Response(None, status.HTTP_200_OK)

        return Response(None, status.HTTP_403_FORBIDDEN)

    def put(self, request):

        new_data = JSONParser().parse(request)
        user = User.objects.get_by_natural_key(request.user)

        try:
            old_data = Orders.objects.get(order_id=new_data["order_id"], customer=user)

        except Orders.DoesNotExist:

            return Response({"Message": "Missing Data"}, status.HTTP_404_NOT_FOUND)

        success, response = alter_order(new_data, old_data, user)

        if success:
            return Response(response)
        else:
            return Response(response, status.HTTP_400_BAD_REQUEST)

