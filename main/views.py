from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .logic.stores import fetch_stores, fetch_items
from .logic.users import *
import json


@api_view(['GET', 'POST'])
def stores(request):

    if request.method == 'POST':
        store = request.data.get("store")

        if not store:
            return Response(None, status.HTTP_400_BAD_REQUEST)

        data = fetch_items(str(store))
    else:
        data = fetch_stores()

    data = json.dumps(data)

    return Response(data, status.HTTP_200_OK)


@api_view(['POST'])
def order(request):

    if request.method == 'POST':
        store = request.data.get("store")

        if not store:
            return Response(None, status.HTTP_400_BAD_REQUEST)

        data = fetch_items(str(store))
    else:
        data = fetch_stores()

    data = json.dumps(data)

    return Response(data, status.HTTP_200_OK)


@api_view(['POST'])
def register_customer(request):

    data = register_user()

    data = json.dumps(data)

    return Response(data, status.HTTP_200_OK)


@api_view(['POST'])
def update_customer(request):

    data = update_user()

    data = json.dumps(data)

    return Response(data, status.HTTP_200_OK)


@api_view(['POST'])
def delete_customer(request):

    data = delete_user()

    data = json.dumps(data)

    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
def fetch_customer(request):

    data = fetch_user()

    data = json.dumps(data)

    return Response(data, status.HTTP_200_OK)
