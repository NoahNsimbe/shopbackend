from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
