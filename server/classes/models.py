from django.db import models
from tlsa_server.models import TLSA_User
from labs.models import Lab
from django.utils.deconstruct import deconstructible
import os
import uuid

@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        # Get the file extension
        ext = filename.split('.')[-1]
        # Generate a random UUID
        filename = f"{uuid.uuid4()}.{ext}"
        # Return the full path
        return os.path.join(self.path, filename)


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


class Experiment(models.Model):
    EXPERIMENT_METHOD_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]

    SUBMISSION_TYPE_CHOICES = [
        ('paper_report', 'Paper Report'),
        ('product_submission', 'Product Submission'),
    ]

    title = models.CharField(max_length=200)
    estimated_time = models.DurationField()
    safety_tags = models.JSONField(default=list)
    experiment_method_tags = models.CharField(max_length=50, choices=EXPERIMENT_METHOD_CHOICES)
    submission_type_tags = models.CharField(max_length=50, choices=SUBMISSION_TYPE_CHOICES)
    other_tags = models.JSONField(default=list)
    description = models.TextField(blank=True, null=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='experiments')

    def __str__(self):
        return self.title
    
class ExperimentImage(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=RandomFileName('experiment_images/'))

    def __str__(self):
        return f"Image for {self.experiment.title}"

class ExperimentFile(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=RandomFileName('experiment_files/'))

    def __str__(self):
        return f"File for {self.experiment.title}"