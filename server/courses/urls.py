from django.urls import path
from .views import CourseView, CourseEnrollmentView, CourseClassView

urlpatterns = [
    path('course', CourseView.as_view(), name='course'),
    path('enroll', CourseEnrollmentView.as_view(), name='course-enrollment'),
    path('classes', CourseClassView.as_view(), name='course-class'),
]