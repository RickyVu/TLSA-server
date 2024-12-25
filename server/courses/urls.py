from django.urls import path
from .views import CourseView, CourseEnrollmentView, CourseClassView, CoursePageListView, CourseSummaryPageView

urlpatterns = [
    path('course', CourseView.as_view(), name='course'),
    path('enroll', CourseEnrollmentView.as_view(), name='course-enrollment'),
    path('classes', CourseClassView.as_view(), name='course-class'),
    path('course-list', CoursePageListView.as_view(), name='frontend-course-list'),
    path('course-summary', CourseSummaryPageView.as_view(), name='course-summmary')
]
