from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import TLSA_User


class Logtests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user(self):
        url = reverse('register')
        data = {
            'username': 'New User',
            'password': '20241211',
            'user_id': '2022999999',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data)  # 重复用户，失败
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # login
        url = reverse('login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 未注册用户，失败
        data = {
            'username': 'New User',
            'password': '20241212',
            'user_id': '2022012080',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
