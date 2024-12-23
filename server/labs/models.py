from django.db import models
from tlsa_server.models import TLSA_User
import os
import uuid
from django.utils.deconstruct import deconstructible

# Random filename generator


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


class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    safety_equipments = models.JSONField(default=list, blank=True, null=True)
    safety_notes = models.TextField(blank=True, null=True)
    lab_image = models.ImageField(upload_to=RandomFileName('lab_images/'), blank=True, null=True)

    def __str__(self):
        return self.name


class ManageLab(models.Model):
    manager = models.ForeignKey(TLSA_User, on_delete=models.CASCADE, to_field='user_id', db_column='manager_user_id')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, to_field='id', db_column='lab_id')

    class Meta:
        db_table = 'manage_lab'

    def __str__(self):
        return f"Manager {self.manager.user_id} manages Lab {self.lab.id}"
