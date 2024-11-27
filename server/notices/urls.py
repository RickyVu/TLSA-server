from django.urls import path
from .views import (
    NoticeView, NoticeCompletionView, NoticeContentView, 
    NoticeTagView, NoticeContentTagView, NoticeRowView
)

urlpatterns = [
    path('notices/notice', NoticeView.as_view(), name='notice'),
    path('notices/completion', NoticeCompletionView.as_view(), name='notice-completion'),
    path('notices/content', NoticeContentView.as_view(), name='notice-content'),
    path('notices/tags', NoticeTagView.as_view(), name='notice-tag'),
    path('notices/content-tags', NoticeContentTagView.as_view(), name='notice-content-tag'),
    path('notices/rows', NoticeRowView.as_view(), name='notice-row'),
]