# classes/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Class
from tlsa_server.models import TLSA_User

class ClassViewTests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.teacher = TLSA_User.objects.create_user(username='teacher', password='testpass')  
        self.teacher.role = 'teacher'      
        self.teacher.save()
        # 创建客户端实例
        self.client = APIClient()
        # 登录教师用户
        self.client.force_authenticate(user=self.teacher)

    def test_create_class(self):
        """
        确保我们可以创建一个新的班级
        """
        url = reverse('class')
        data = {
            'name': 'New Class',
            'start_time': '2024-11-27 11:40:58.801197+00',
            'created_at': '2024-11-27 11:40:58.801197+00',
            'updated_at': '2024-11-27 11:40:58.801197+00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Class.objects.count(), 1)
        self.assertEqual(Class.objects.get().name, 'New Class')

    def test_get_class(self):
        """
        确保我们可以获取班级列表
        """
        # 创建一个班级用于测试
        Class.objects.create(name='Test Class', start_time = '2024-11-27 11:40:58.801197+00')
        url = reverse('class')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Class')

    def test_get_class_by_id(self):
        """
        确保我们可以通过ID获取特定的班级
        """
        class_instance = Class.objects.create(name='Test Class', start_time = '2024-11-27 11:40:58.801197+00')
        url = f'{reverse("class")}?class_id={class_instance.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Class')

    def test_get_class_by_name(self):
        """
        确保我们可以通过名称获取班级
        """
        Class.objects.create(name='Test Class', start_time = '2024-11-27 11:40:58.801197+00')
        url = f'{reverse("class")}?class_name=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Class')
