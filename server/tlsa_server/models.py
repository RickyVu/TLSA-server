from django.contrib.auth.models import AbstractUser
from django.db import models

class TLSA_User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('manager', 'Manager'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)