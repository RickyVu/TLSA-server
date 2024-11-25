from django.db import models

# Create your models here.
from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_time = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name