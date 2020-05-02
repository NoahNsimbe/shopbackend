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
from .logic.users import create_user, update_account, fetch_user

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def test(request):
    data = JSONParser().parse(request)
    g = data["f"]

    return Response("")


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

    data = JSONParser().parse(request)

    try:
        username = data["username"]
        email = data["email"]
        password = data["password"]

    except KeyError:
        return Response({"Message": "Missing Data"}, status.HTTP_400_BAD_REQUEST)

    user = UserClass()
    user.register(username, password, email)

    success, message = create_user(user)

    if success:
        return Response(None, status.HTTP_201_CREATED)

    return Response({"Message": message}, status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = fetch_user(str(request.user))
        return Response(data)

    def put(self, request):

        data = JSONParser().parse(request)

        user = UserClass()
        user.load(data)
        user.userName = str(request.user)

        success, message = update_account(user)

        if success:
            return Response(None)
        else:
            return Response(message, status.HTTP_400_BAD_REQUEST)

    def delete(self):
        return


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = fetch_orders(str(request.user))
        return Response(data)

    def post(self, request):

        data = JSONParser().parse(request)

        user_order = OrderClass()
        user_order.load(data)
        user_order.customer = str(request.user)

        logger.error(user_order)

        success, message = place_order(user_order)

        if success:
            return Response(None, status.HTTP_201_CREATED)
        else:
            return Response(message, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        data = JSONParser().parse(request)

        user_order = OrderClass()
        user_order.load(data)

        if delete_order(user_order):
            return Response(None, status.HTTP_200_OK)

        return Response(None, status.HTTP_403_FORBIDDEN)

    def put(self, request):

        data = JSONParser().parse(request)

        user_order = OrderClass()
        user_order.load(data)
        user_order.customer = str(request.user)

        success, message = alter_order(user_order)

        if success:
            return Response(None)
        else:
            return Response(message, status.HTTP_403_FORBIDDEN)

