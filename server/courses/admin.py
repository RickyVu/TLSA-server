from django.contrib import admin
from .models import Course, CourseClass, CourseEnrollment

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseClass)
admin.site.register(CourseEnrollment)