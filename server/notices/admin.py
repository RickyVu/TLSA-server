from django.contrib import admin
from .models import (Notice,
                     NoticeCompletion,
                     NoticeContent,
                     NoticeContentTag,
                     NoticeRow,
                     NoticeTag)

# Register your models here.
admin.site.register(Notice)
admin.site.register(NoticeCompletion)
admin.site.register(NoticeContent)
admin.site.register(NoticeContentTag)
admin.site.register(NoticeRow)
admin.site.register(NoticeTag)
