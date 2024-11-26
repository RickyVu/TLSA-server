from django.db import models
from tlsa_server.models import TLSA_User
from classes.models import Class

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CourseEnrollment(models.Model):
    student = models.ForeignKey(TLSA_User, on_delete=models.CASCADE, to_field='id', db_column='student_id')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, to_field='id', db_column='course_id')

    class Meta:
        db_table = 'course_enrollment'

    def __str__(self):
        return f"Student {self.student.id} enrolled in Course {self.course.id}"

class CourseClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, to_field='id', db_column='course_id')
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, to_field='id', db_column='class_id')

    class Meta:
        db_table = 'course_class'

    def __str__(self):
        return f"Course {self.course.id} has Class {self.class_instance.id}"