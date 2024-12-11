# classes/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Course,CourseClass,CourseEnrollment
from classes.models import Class
from tlsa_server.models import TLSA_User

class CourseViewTests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.teacher = TLSA_User.objects.create_user(username='teacher', password='testpass')  
        self.teacher.role = 'teacher'      
        self.teacher.save()
        # 创建客户端实例
        self.client = APIClient()
        # 登录教师用户
        self.client.force_authenticate(user=self.teacher)

    def test_create_course(self):
        """
        确保我们可以创建一个新的班级
        """
        url = reverse('course')
        data = {
            'name': 'New Course',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().name, 'New Course')

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

    def test_post_course(self):

        url = reverse('course')
        data = {
            'name': 'test'
        }
        response = self.client.post(url, data,format = None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['course']['name'],'test')

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

        cse = Course.objects.create(name='New Course')
        cls = Class.objects.create(name='New Class',
                      start_time = '2024-11-27 11:40:58.801197+00',
                      created_at = '2024-11-27 11:40:58.801197+00',
                      updated_at = '2024-11-27 11:40:58.801197+00')

        course_class = CourseClass.objects.create(
            course=cse,
            class_instance=cls
        )

        course_class_from_db = CourseClass.objects.get(id=course_class.id)
        self.assertEqual(course_class_from_db.course, cse)
        self.assertEqual(course_class_from_db.class_instance, cls)
    
    def test_post_courseclass(self):

        cse = Course.objects.create(name='New Course')
        cls = Class.objects.create(name='New Class',
                      start_time = '2024-11-27 11:40:58.801197+00',
                      created_at = '2024-11-27 11:40:58.801197+00',
                      updated_at = '2024-11-27 11:40:58.801197+00')

        data = {          
            'class_id' : cls.id,
            'course_id' : cse.id
        }
        url = reverse('course-class')
        response = self.client.post(url, data,format = None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['course_class']['course_id'], cse.id)


    def test_create_classenrollment(self):

        stt = TLSA_User.objects.create(role = 'student')
        cse = Course.objects.create(name='New Course')

        course_class = CourseEnrollment.objects.create(
            student=stt,
            course=cse
        )

        course_enrollment_from_db = CourseEnrollment.objects.get(id=course_class.id)
        self.assertEqual(course_enrollment_from_db.student, stt)
        self.assertEqual(course_enrollment_from_db.course, cse)

    def test_post_classenrollment(self):

        stt = TLSA_User.objects.create(role = 'student')
        cse = Course.objects.create(name='New Course')

        data = {          
            'student_ids' : [stt.id],
            'course_id' : cse.id
        }
        url = reverse('course-enrollment')
        response = self.client.post(url, data,format = None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['enrollment']['course_id'], cse.id)
