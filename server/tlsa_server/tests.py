from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import TLSA_User
from django.core.files.uploadedfile import SimpleUploadedFile

class Logtests(APITestCase):
    def setUp(self):
        self.affair = TLSA_User.objects.create_user(username='manager', password='testpass', user_id='2022012080')
        self.affair.role = 'teachingAffairs'
        self.affair.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.affair)

        self.teacher = TLSA_User.objects.create_user(username='teacher', password='testpass', user_id='2022012082')
        self.teacher.role = 'teacher'
        self.teacher.save()
        self.client_2 = APIClient()
        self.client_2.force_authenticate(user=self.teacher)

    def test_user(self):
        url = reverse('register')
        data={
            "user_id": "2021000000",
            "password": "123456",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data)  # 重复用户，失败
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('register-staff')
        data={
            "user_id": "2022000000",
            "password": "123456",
            "role": "teacher"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # login
        url = reverse('login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 未注册用户，失败
        data={
            "user_id": "2021000001",
            "password": "123456",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user(self):
        url = reverse('register')
        data={
            "user_id": "2021000000",
            "password": "123456",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = f"{reverse('user-info')}?user_id=2021000000"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

