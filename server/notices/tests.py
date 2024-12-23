# classes/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Notice,NoticeCompletion,NoticeContent,NoticeTag,NoticeContentTag,NoticeRow
from classes.models import Class
from tlsa_server.models import TLSA_User
import time

class NoticeViewTests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.manager = TLSA_User.objects.create_user(username='manager', password='testpass', user_id='2022012080')
        self.manager.role = 'manager'
        self.manager.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.manager)

        self.student = TLSA_User.objects.create_user(username='student', password='testpass', user_id='2022012081')
        self.student.role = 'student'
        self.student.save()

        self.teacher = TLSA_User.objects.create_user(username='teacher', password='testpass', user_id='2022012082')
        self.teacher.role = 'teacher'
        self.teacher.save()

        self.client_1 = APIClient()
        self.client_1.force_authenticate(user=self.student)

        self.client_2 = APIClient()
        self.client_2.force_authenticate(user=self.teacher)

        # 创建测试数据
        self.user = self.manager
        
        self.data = {
            'class_or_lab_id': 1,
            'sender': self.user.user_id,
            'notice_type': 'class',
            'post_time':'2024-11-27 11:40:58.801197+00',
            'end_time':'2024-11-27 11:40:58.801197+00',
        }
        self.data2 = {
            'class_or_lab_id': 2,
            'sender': self.user.user_id,
            'notice_type': 'lab',
            'post_time':'2024-11-27 11:40:58.801197+00',
            'end_time':'2024-11-27 11:40:58.801197+00',
        }
        self.url = reverse('notice-list')
        self.notice1 = self.client.post(self.url, self.data)
        self.notice2 = self.client.post(self.url, self.data2)
        

    def test_notice_creation(self):
        # 测试通知是否创建成功
        # print(self.notice1.data['notice'])
        self.assertEqual(self.notice1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.notice2.status_code, status.HTTP_201_CREATED)

    def test_get_notices_no_filters(self):
        # 测试没有查询参数的情况
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 应该返回所有通知

    def test_get_notices_by_id(self):
        # 测试通过 notice_id 过滤
        response = self.client.get(self.url, {'notice_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notices_by_type(self):
        # 测试通过 notice_type 过滤
        response = self.client.get(self.url, {'notice_type': 'class'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['notice_type'], 'class')

    def test_get_notices_by_class_or_lab_id(self):
        # 测试通过 class_or_lab_id 过滤
        response = self.client.get(self.url, {'class_or_lab_id': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['class_or_lab_id'], 1)

    def test_get_notices_combined_filters(self):
        # 测试组合过滤条件
        response = self.client.get(self.url, {'notice_type': 'class', 'class_or_lab_id': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['notice_type'], 'class')
        self.assertEqual(response.data[0]['class_or_lab_id'], 1)
    
    def test_patch_notice(self):
        data = {
            'id':1,
            'class_or_lab_id': 2,
            'sender': self.user.user_id,
            'notice_type': 'lab',
            'post_time':'2024-11-27 11:40:58.801197+00',
            'end_time':'2024-11-27 11:40:58.801197+00',
        }
        invalid_data = {
            'id':4,
            'class_or_lab_id': 2,
            'sender': self.user.user_id,
            'notice_type': 'lab',
            'post_time':'2024-11-27 11:40:58.801197+00',
            'end_time':'2024-11-27 11:40:58.801197+00',
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response1 = self.client.patch(self.url, invalid_data)
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_notice(self):
        self.data3 = {
            'class_or_lab_id': 2,
            'sender': self.user.user_id,
            'notice_type': 'lab',
            'post_time':'2024-11-27 11:40:58.801197+00',
            'end_time':'2024-11-27 11:40:58.801197+00',
        }
        self.notice3 = self.client.post(self.url, self.data3)
        url = f'{reverse("notice-list")}?notice_id=3'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        

