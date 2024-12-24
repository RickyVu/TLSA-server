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


class Notice(models.Model):
    NOTICE_TYPE_CHOICES = [
        ('class', 'Class'),
        ('lab', 'Lab'),
    ]

    class_or_lab_id = models.IntegerField()
    sender = models.ForeignKey(
        TLSA_User,
        on_delete=models.CASCADE,
        to_field='user_id',
        related_name='notices_sent',
        verbose_name="Sender"
    )
    notice_type = models.CharField(max_length=10, choices=NOTICE_TYPE_CHOICES)
    post_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notice {self.id} by {self.sender.user_id} ({self.notice_type})"


class NoticeCompletion(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='completions')
    user = models.ForeignKey(
        TLSA_User,
        on_delete=models.CASCADE,
        to_field='user_id',
        related_name='notice_completions',
        verbose_name="User"
    )
    completion_time = models.DateTimeField()

    def __str__(self):
        return f"Notice {self.notice.id} completed by {self.user.user_id}"


class NoticeContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    ]

    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    text_content = models.TextField(blank=True, null=True)  # For text content
    image_content = models.ImageField(upload_to=DateTimeFileName('notice_images/'), blank=True, null=True)  # For image content
    file_content = models.FileField(upload_to=DateTimeFileName('notice_files/'), blank=True, null=True)  # For file content

    def __str__(self):
        return f"Content {self.id} ({self.content_type})"


class NoticeTag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name


class NoticeContentTag(models.Model):
    notice_content_id = models.ForeignKey(NoticeContent, on_delete=models.CASCADE)
    notice_tag_id = models.ForeignKey(NoticeTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('notice_content_id', 'notice_tag_id')


class NoticeRow(models.Model):
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='rows')
    notice_content_id = models.ForeignKey(NoticeContent, on_delete=models.CASCADE)
    order_num = models.IntegerField()

    class Meta:
        unique_together = ('notice_id', 'notice_content_id')
