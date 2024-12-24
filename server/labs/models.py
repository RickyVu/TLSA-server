from django.db import models
from tlsa_server.models import TLSA_User
import os
from datetime import datetime
from django.utils.deconstruct import deconstructible


@deconstructible
class DateTimeFileName(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        # Get the file extension
        ext = filename.split('.')[-1]

        # Get the original filename (without extension)
        original_name = os.path.splitext(filename)[0]

        # Get the current datetime in a readable format
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the new filename
        new_filename = f"{original_name}-{current_datetime}.{ext}"

        # Return the full path
        return os.path.join(self.path, new_filename)


class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    safety_equipments = models.JSONField(default=list, blank=True, null=True)
    safety_notes = models.TextField(blank=True, null=True)
    lab_image = models.ImageField(upload_to=DateTimeFileName('lab_images/'), blank=True, null=True)
    map_image = models.ImageField(upload_to=DateTimeFileName('lab_map/'), blank=True, null=True)

    def __str__(self):
        return self.name


class ManageLab(models.Model):
    manager = models.ForeignKey(TLSA_User, on_delete=models.CASCADE, to_field='user_id', db_column='manager_user_id')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, to_field='id', db_column='lab_id')

    class Meta:
        db_table = 'manage_lab'

    def __str__(self):
        return f"Manager {self.manager.user_id} manages Lab {self.lab.id}"
