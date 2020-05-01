from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .logic.models import UserClass, OrderClass
from .logic.orders import fetch_orders, place_order, delete_order, alter_order
from .logic.stores import fetch_stores, fetch_items
import json
import logging
from .logic.users import create_user

logger = logging.getLogger(__name__)


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


@api_view(['POST'])
def register(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    user = UserClass()
    user.register(username, password, email)

    if create_user(user):
        return Response(None, status.HTTP_201_CREATED)
    else:

        return Response({"Message": "Missing Data"}, status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        # data = json.dumps(user)
        content = {"user": str(user)}
        logger.error(user)
        return Response(content)

    def post(self, request):
        user = request.user
        data = json.dumps(user)
        return Response(data, status.HTTP_200_OK)

    def put(self, request):
        return

    def delete(self):
        return


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = fetch_orders(request.user)
        return Response(data)

    def post(self, request):
        # store = request.data.get("store")
        order_data = JSONParser().parse(request)
        logger.error(order_data)

        user_order = OrderClass()
        user_order.customer = str(request.user)
        user_order.load(request.data)

        if place_order(user_order):
            return Response(None, status.HTTP_201_CREATED)

        return Response(None, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):

        user_order = OrderClass()
        user_order.load(request.data)

        if delete_order(user_order):
            return Response(None, status.HTTP_200_OK)

        return Response(None, status.HTTP_403_FORBIDDEN)

    def put(self, request):

        user_order = OrderClass()
        user_order.customer = str(request.user)
        user_order.load(request.data)

        if alter_order(user_order):
            return Response(None, status.HTTP_200_OK)

        return Response(None, status.HTTP_403_FORBIDDEN)
