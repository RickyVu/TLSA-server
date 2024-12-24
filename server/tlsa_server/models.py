from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
import os
from datetime import datetime
from django.utils.deconstruct import deconstructible

# Custom validator to ensure the user_id contains only numbers
numeric_validator = RegexValidator(
    regex=r'^\d{10}$',  # Exactly 10 digits
    message="user_id must be exactly 10 digits and contain only numbers."
)

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

class TLSA_User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('manager', 'Manager'),
        ('teachingAffairs', 'TeachingAffairs')
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=DateTimeFileName('profile_pics/'), blank=True, null=True)
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
            self.username = self.user_id
        super().save(*args, **kwargs)

    # Override the default primary key behavior
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'tlsa_user'

    def __str__(self):
        return f"{self.real_name} ({self.user_id})"