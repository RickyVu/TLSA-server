# classes/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Lab,ManageLab
from tlsa_server.models import TLSA_User

class CourseViewTests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.manager = TLSA_User.objects.create_user(username='manager', password='testpass')  
        self.manager.role = 'manager'      
        self.manager.save()
        # 创建客户端实例
        self.client = APIClient()
        # 登录教师用户
        self.client.force_authenticate(user=self.manager)

    def test_create_lab(self):
        """
        确保我们可以创建一个新的班级
        """
        url = reverse('lab')
        data = {
            'name': 'New Lab',
            'location': '6A116'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lab.objects.count(), 1)
        self.assertEqual(Lab.objects.get().name, 'New Lab')
        self.assertEqual(Lab.objects.get().location, '6A116')

    def test_get_lab(self):
        """
        确保我们可以获取班级列表
        """
        # 创建一个班级用于测试
        Lab.objects.create(name='Test Lab')
        url = reverse('lab')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Lab')

    def test_get_lab_by_id(self):
        """
        确保我们可以通过ID获取特定的班级
        """
        lab_instance = Lab.objects.create(name='Test Lab')
        url = f'{reverse("lab")}?lab_id={lab_instance.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Lab')

    def test_get_lab_by_name(self):
        """
        确保我们可以通过名称获取班级
        """
        Lab.objects.create(name='Test Lab')
        url = f'{reverse("lab")}?lab_name=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Lab')

    def test_create_managelab(self):
        mng = TLSA_User.objects.create(role = "manager")
        laB = Lab.objects.create(name='Test Lab')

        manage_lab = ManageLab.objects.create(
            manager=mng,
            lab = laB
        )

        manage_lab_from_db = ManageLab.objects.get(id=manage_lab.id)
        self.assertEqual(manage_lab_from_db.manager, mng)
        self.assertEqual(manage_lab_from_db.lab, laB)

    def test_get_managelab(self):

        mng = TLSA_User.objects.create(role = "manager")
        laB = Lab.objects.create(name='Test Lab')

        ManageLab.objects.create(
            manager=mng,
            lab = laB
        )

        url = reverse('lab-manager')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['lab_id'],laB.id)

    def test_post_managelab(self):
        
        mng = TLSA_User.objects.create(role = "manager")
        laB = Lab.objects.create(name='Test Lab')

        url = reverse('lab-manager')
        data = {
            'manager_id': mng.id,
            'lab_id': laB.id
        }
        response = self.client.post(url, data,format = None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['manager']['manager_id'],mng.id)