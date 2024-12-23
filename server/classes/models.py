from django.db import models
from tlsa_server.models import TLSA_User
from labs.models import Lab
# Create your models here.


class Class(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ClassLocation(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    lab_id = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return f"Class {self.class_id} at Lab {self.lab_id}"


class TeachClass(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(TLSA_User, to_field='user_id', on_delete=models.CASCADE)

    def __str__(self):
        return f"Teacher {self.teacher_id} teaches Class {self.class_id}"


class ClassComment(models.Model):
    sender_id = models.ForeignKey(TLSA_User, to_field='user_id', on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    sent_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.sender_id} on Class {self.class_id}"
