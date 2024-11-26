from django.db import models
from django.utils import timezone
# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name