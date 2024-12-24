# classes/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Class, Experiment
from labs.models import Lab
from tlsa_server.models import TLSA_User


class ClassViewTests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.teacher = TLSA_User.objects.create_user(username='teacher', password='testpass', user_id='2022012080')
        self.teacher.role = 'teacher'
        self.teacher.save()
        # 创建客户端实例
        self.client = APIClient()
        # 登录教师用户
        self.client.force_authenticate(user=self.teacher)

        self.student = TLSA_User.objects.create_user(username='student', password='testpass', user_id='2022012081')
        self.student.role = 'student'
        self.student.save()

        self.manager = TLSA_User.objects.create_user(username='manager', password='testpass', user_id='2022012082')
        self.manager.role = 'manager'
        self.manager.save()

        self.client_secure1 = APIClient()
        self.client_secure1.force_authenticate(user=self.student)

        self.client_secure2 = APIClient()
        self.client_secure2.force_authenticate(user=self.manager)

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

    def test_create_class_secure(self):
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
        response = self.client_secure1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client_secure2.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_class(self):
        """
        确保我们可以获取班级列表
        """
        # 创建一个班级用于测试
        Class.objects.create(name='Test Class', start_time='2024-11-27 11:40:58.801197+00')
        url = reverse('class')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Class')

    def test_get_class_by_id(self):
        """
        确保我们可以通过ID获取特定的班级
        """
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        url = f'{reverse("class")}?class_id={class_instance.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Class')

    def test_get_class_by_name(self):
        """
        确保我们可以通过名称获取班级
        """
        Class.objects.create(name='Test Class',
                             start_time='2024-11-27 11:40:58.801197+00',
                             created_at='2024-11-27 11:40:58.801197+00',
                             updated_at='2024-11-27 11:40:58.801197+00')
        url = f'{reverse("class")}?class_name=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Class')

    def test_create_teacherclass(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        url = reverse('teach-class')
        data = {
            'class_id': class_instance.id,
            'teacher_id': self.teacher.user_id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_teacherclass(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        url = reverse('teach-class')
        data = {
            'class_id': class_instance.id,
            'teacher_id': self.teacher.user_id
        }
        response = self.client.post(url, data)
        url = f'{reverse('teach-class')}?class_id={class_instance.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_teacherclass(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        url = reverse('teach-class')
        data = {
            'class_id': class_instance.id,
            'teacher_id': self.teacher.user_id
        }
        response = self.client.post(url, data)
        url = f'{reverse('teach-class')}?class_id={class_instance.id}&teacher_id={self.teacher.user_id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_classlocation(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        lab_instance = Lab.objects.create(name='Test Lab')
        url = reverse('class-location')
        data = {
            'class_id': class_instance.id,
            'lab_id': lab_instance.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_classlocation(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        lab_instance = Lab.objects.create(name='Test Lab')
        url = reverse('class-location')
        data = {
            'class_id': class_instance.id,
            'lab_id': lab_instance.id
        }
        response = self.client.post(url, data)
        url = f'{reverse('class-location')}?class_id={class_instance.id}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_classlocation(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        lab_instance = Lab.objects.create(name='Test Lab')
        url = reverse('class-location')
        data = {
            'class_id': class_instance.id,
            'lab_id': lab_instance.id
        }
        response = self.client.post(url, data)
        url = f'{reverse('class-location')}?class_id={class_instance.id}&lab_id={lab_instance.id}'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_experiment(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        data = {
            "title": "experiment",
            "estimated_time": 1,
            "safety_tags": ["1", "2", "3"],
            "experiment_method_tags": "individual",
            "submission_type_tags": "paper_report",
            "other_tags": ["1", "2", "3"],
            "description": "use_git",
            "class_id": class_instance.id,
            "images": ["image1.jpg", "image2.jpg"],
            "files": ["instructions.pdf", "data_sheet.xlsx"]
        }

        data1 = {
            "id": 1,
            "title": "experiment",
            "estimated_time": 1,
            "safety_tags": ["1", "2", "3"],
            "experiment_method_tags": "group",
            "submission_type_tags": "paper_report",
            "other_tags": ["1", "2", "3"],
            "description": "use_git",
            "class_id": class_instance.id,
            "images": ["image1.jpg", "image2.jpg"],
            "files": ["instructions.pdf", "data_sheet.xlsx"]
        }

        url = reverse('experiment-list')
        response0 = self.client.post(url, data)
        self.assertEqual(response0.status_code, status.HTTP_201_CREATED)

        response1 = self.client.patch(url, data1)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        url = f'{reverse('experiment-list')}?class_id = {class_instance.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = f'{reverse('experiment-list')}?experiment_id={1}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_commenttoclass(self):
        class_instance = Class.objects.create(name='Test Class',
                                              start_time='2024-11-27 11:40:58.801197+00',
                                              created_at='2024-11-27 11:40:58.801197+00',
                                              updated_at='2024-11-27 11:40:58.801197+00')
        url = reverse('class-comments')
        data = {
            'class_id': class_instance.id,
            'content': 'test',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = f'{reverse('class-comments')}?class_id={class_instance.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = f'{reverse('class-comments')}?class_id={class_instance.id}&sender_id={self.teacher.user_id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
