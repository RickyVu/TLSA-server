# classes/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Course, CourseClass, CourseEnrollment
from classes.models import Class
from tlsa_server.models import TLSA_User
from .views import CourseView


class CourseViewTests(APITestCase):
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
        self.client_secure1 = APIClient()
        self.client_secure1.force_authenticate(user=self.student)

        self.manager = TLSA_User.objects.create_user(username='manager', password='testpass', user_id='2022012082')
        self.manager.role = 'manager'
        self.manager.save()
        self.client_secure2 = APIClient()
        self.client_secure2.force_authenticate(user=self.manager)

    def test_create_course(self):
        """
        确保我们可以创建一个新的班级
        """
        url = reverse('course')
        data = {
            'course_code': '00000001',
            'course_sequence': '12345',
            'department': '教学楼',
            'name': 'New Course',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().name, 'New Course')

    def test_patch_course(self):
        """
        确保我们可以创建一个新的班级
        """
        url = reverse('course')
        data = {
            'course_code': '00000001',
            'course_sequence': '12345',
            'department': '教学楼',
            'name': 'New Course',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'course_code': '00000001',
            'course_sequence': '12345',
            'department': '九十教',
            'name': 'Old Course',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_secure(self):
        """
        确保我们可以创建一个新的班级
        """
        url = reverse('course')
        data = {
            'course_code': '00000001',
            'course_sequence': '12345',
            'department': '教学楼',
            'name': 'New Course',
        }
        response = self.client_secure1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client_secure2.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course(self):
        """
        确保我们可以获取班级列表
        """
        # 创建一个班级用于测试
        Course.objects.create(name='Test Course')
        url = reverse('course')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Course')

    def test_get_course_by_id(self):
        """
        确保我们可以通过ID获取特定的班级
        """
        course_instance = Course.objects.create(name='Test Course')
        url = f'{reverse("course")}?course_id={course_instance.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Course')

    def test_get_course_by_name(self):
        """
        确保我们可以通过名称获取班级
        """
        Course.objects.create(name='Test Course')
        url = f'{reverse("course")}?course_name=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Course')

    def test_create_courseclass(self):

        cse = Course.objects.create(course_code='00000001',
                                    course_sequence='12345',
                                    department='教学楼',
                                    name='New Course'
                                    )
        cls = Class.objects.create(name='New Class',
                                   start_time='2024-11-27 11:40:58.801197+00',
                                   created_at='2024-11-27 11:40:58.801197+00',
                                   updated_at='2024-11-27 11:40:58.801197+00')

        url = reverse('course-class')
        data = {
            'class_id': cls.id,
            'course_code': cse.course_code,
            'course_sequence': cse.course_sequence
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_courseclass_secure(self):

        cse = Course.objects.create(course_code='00000001',
                                    course_sequence='12345',
                                    department='教学楼',
                                    name='New Course')
        cls = Class.objects.create(name='New Class',
                                   start_time='2024-11-27 11:40:58.801197+00',
                                   created_at='2024-11-27 11:40:58.801197+00',
                                   updated_at='2024-11-27 11:40:58.801197+00')

        url = reverse('course-class')
        data = {
            'class_id': cls.id,
            'course_code': cse.course_code,
            'course_sequence': cse.course_sequence
        }

        response = self.client_secure1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client_secure2.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_classenrollment(self):

        stt = self.student
        cse = Course.objects.create(course_code='00000001',
                                    course_sequence='12345',
                                    department='教学楼',
                                    name='New Course')

        data = {
            'student_user_ids': [stt.user_id],
            'course_code': cse.course_code,
            'course_sequence': cse.course_sequence
        }
        url = reverse('course-enrollment')
        response = self.client.post(url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['enrollment']['course_id'], cse.id)

        view = CourseView()
        response = view._get_personal_courses_filters(self.student)
        self.assertEqual(response, {'course_code__in': ('00000001',), 'course_sequence__in': ('12345',)})

    def test_create_classenrollment_secure(self):

        stt = self.student
        cse = Course.objects.create(course_code='00000001',
                                    course_sequence='12345',
                                    department='教学楼',
                                    name='New Course')

        data = {
            'student_ids': [stt.id],
            'course_id': cse.id
        }
        url = reverse('course-enrollment')
        response = self.client_secure1.post(url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client_secure1.post(url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
