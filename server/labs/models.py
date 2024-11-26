from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Manage_Lab(models.Model):
    manager_id = models.CharField(max_length=100)
    lab_id = models.IntegerField()

    def __str__(self):
        return f"Manage ID: {self.manager_id}, Lab ID: {self.lab_id}"
    
class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    #manager = ArrayField(models.CharField(), blank=True, null=True)
    def __str__(self):
        return self.name