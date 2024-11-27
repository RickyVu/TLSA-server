from django.db import models

class Notice(models.Model):
    class_or_lab_id = models.IntegerField()
    sender_id = models.CharField(max_length=10)
    notice_type = models.CharField(max_length=10, choices=[('class', 'Class'), ('lab', 'Lab')])
    post_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NoticeCompletion(models.Model):
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=10)
    completion_time = models.DateTimeField()

class NoticeContent(models.Model):
    content = models.TextField()
    content_type = models.CharField(max_length=50)

class NoticeTag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

class NoticeContentTag(models.Model):
    notice_content_id = models.ForeignKey(NoticeContent, on_delete=models.CASCADE)
    notice_tag_id = models.ForeignKey(NoticeTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('notice_content_id', 'notice_tag_id')

class NoticeRow(models.Model):
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE)
    notice_content_id = models.ForeignKey(NoticeContent, on_delete=models.CASCADE)
    order_num = models.IntegerField()

    class Meta:
        unique_together = ('notice_id', 'notice_content_id')