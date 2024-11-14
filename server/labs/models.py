from django.db import models

# Create your models here.
from django.db import models

class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name