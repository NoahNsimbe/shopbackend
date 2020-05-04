import json
import os
import string
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import random


class StoresTestCase(APITestCase):

    fixtures = ['dump.json']
    url = reverse('stores')

    def test_get_stores(self):

        _get_pass = self.client.get(self.url, None, format='json')

        self.assertEqual(_get_pass.status_code, status.HTTP_200_OK)

    def test_get_items(self):

        _post_fail = self.client.post(self.url, None, format='json')
        _post_pass = self.client.post(self.url, {"store": "stores"}, format='json')

        self.assertEqual(_post_pass.status_code, status.HTTP_200_OK)
        self.assertEqual(_post_fail.status_code, status.HTTP_400_BAD_REQUEST)


class AuthTestCase(APITestCase):
    data_path = os.path.basename(os.path.dirname(__file__))
    data_file = os.path.join(data_path, "test.json")
    input_data = json.load(open(data_file))

    fixtures = ['dump.json']
    access_token = ""
    refresh_token = ""

    get_token_url = reverse('token_obtain_pair')
    verify_token_url = reverse('token_verify')

    def setUp(self):
        self.test_get_token()

    def test_get_token(self):

        data = {
            "username": self.input_data["account_info"]["username"],
            "password": self.input_data["account_info"]["password"]
        }

        resp = self.client.post(self.get_token_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        self.assertTrue('refresh' in resp.data)
        self.access_token = resp.data['access']
        self.refresh_token = resp.data['refresh']

    def test_verify_token(self):

        resp = self.client.post(self.verify_token_url, {"access": self.access_token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(self.verify_token_url, {'access': 'invalid'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):

        resp = self.client.post(self.get_token_url, {"refresh": self.refresh_token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['token'] != self.access_token)


class UserTestCase(APITestCase):

    data_path = os.path.basename(os.path.dirname(__file__))
    data_file = os.path.join(data_path, "test.json")
    input_data = json.load(open(data_file))

    user_url = reverse('user')
    register_url = reverse('register')
    get_token_url = reverse('token_obtain_pair')

    username = ""
    token = ""

    def setUp(self):
        self.test_register()

    def get_token(self):

        data = {
            "username": self.username,
            "password": self.username
        }
        resp = self.client.post(self.get_token_url, data, format='json')

        self.token = resp.data['access']

    def test_register(self):
        _letters = string.ascii_letters
        self.username = ''.join(random.choice(_letters) for _ in range(8))

        self.input_data["register"]["username"] = self.username
        self.input_data["register"]["password"] = self.username

        _success = self.client.post(self.register_url, self.input_data["register"], format='json')
        self.assertEqual(_success.status_code, status.HTTP_201_CREATED)

        self.get_token()

    def test_update_info(self):

        _success = self.client.put(self.user_url, self.input_data["user_info"], format='json')
        self.assertEqual(_success.status_code, status.HTTP_200_OK)

    def test_deactivate_account(self):

        _success = self.client.delete(self.user_url, {"password": self.username}, format='json')
        self.assertEqual(_success.status_code, status.HTTP_204_NO_CONTENT)


class OrderTestCase(APITestCase):

    data_path = os.path.basename(os.path.dirname(__file__))
    data_file = os.path.join(data_path, "test.json")
    input_data = json.load(open(data_file))

    fixtures = ['dump.json']

    url = reverse('order')
    get_token_url = reverse('token_obtain_pair')
    token = ""

    order = None

    def setUp(self):
        data = {
            "username": self.input_data["account_info"]["username"],
            "password": self.input_data["account_info"]["password"]
        }
        resp = self.client.post(self.get_token_url, data, format='json')
        self.token = resp.data['access']

    def test_place_order(self):
        resp = self.client.post(self.url, self.input_data["place_order"], format='json')
        self.order = resp.data

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_order(self):
        resp = self.client.post(self.url, self.order, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) >= 1)

    def test_change_order(self):

        data = self.input_data["change_order"]
        data["order_id"] = self.order["order_id"]

        resp = self.client.post(self.url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) == 1)
        self.assertTrue(resp.data != self.order["order_id"])

    def test_delete_order(self):

        data = None

        resp = self.client.delete(self.url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
