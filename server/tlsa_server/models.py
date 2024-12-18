from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
import os
import uuid
from django.utils.deconstruct import deconstructible

# Custom validator to ensure the user_id contains only numbers
numeric_validator = RegexValidator(
    regex=r'^\d{10}$',  # Exactly 10 digits
    message="user_id must be exactly 10 digits and contain only numbers."
)

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

class TLSA_User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('manager', 'Manager'),
        ('teachingAffairs', 'TeachingAffairs')
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=RandomFileName('profile_pics/'), blank=True, null=True)
    real_name = models.CharField(max_length=150, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)

    user_id = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="User ID",
        validators=[
            MinLengthValidator(10),  # Ensure exactly 10 characters
            MaxLengthValidator(10),  # Ensure exactly 10 characters
            numeric_validator,  # Ensure only numbers
        ]
    )

    # Set the custom user ID as the primary key
    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.user_id
        super().save(*args, **kwargs)

    # Override the default primary key behavior
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'tlsa_user'