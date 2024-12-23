from django.db import models
from tlsa_server.models import TLSA_User
from classes.models import Class
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class Course(models.Model):
    course_code = models.CharField(max_length=8, verbose_name="Course Code")  # 课程号 (8 characters)
    course_sequence = models.CharField(max_length=5, verbose_name="Course Sequence")  # 课序号 (1-5 characters)
    department = models.CharField(max_length=50, verbose_name="Department")
    name = models.CharField(max_length=100, verbose_name="Course Name")

    class Meta:
        unique_together = ('course_code', 'course_sequence')  # Composite primary key
        db_table = 'course'

    def __str__(self):
        return f"{self.course_code}-{self.course_sequence} ({self.name})"


class CourseEnrollment(models.Model):
    student = models.ForeignKey(
        TLSA_User,
        on_delete=models.CASCADE,
        to_field='user_id',
        db_column='student_user_id',
        verbose_name="Student"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    class Meta:
        unique_together = ('student', 'course')
        db_table = 'course_enrollment'

    def __str__(self):
        return f"Student {self.student.user_id} enrolled in Course {self.course.course_code}-{self.course.course_sequence}"


class CourseClass(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='classes'
    )
    class_instance = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        to_field='id',
        db_column='class_id'
    )

    class Meta:
        unique_together = ('course', 'class_instance')
        db_table = 'course_class'

    def __str__(self):
        return f"Course {self.course.course_code}-{self.course.course_sequence} has Class {self.class_instance.id}"
