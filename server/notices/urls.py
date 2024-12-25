from django.urls import path
from .views import (NoticeView, 
                    NoticeCompletionView, 
                    NoticeContentView, 
                    NoticeTagView, 
                    NoticeContentTagView, 
                    NoticeRowView,
                    NoticePageView)

urlpatterns = [
    path('notices', NoticeView.as_view(), name='notice-list'),
    path('notice-completions', NoticeCompletionView.as_view(), name='notice-completion-list'),
    path('notice-contents', NoticeContentView.as_view(), name='notice-content-list'),
    path('notice-tags', NoticeTagView.as_view(), name='notice-tag-list'),
    path('notice-content-tags', NoticeContentTagView.as_view(), name='notice-content-tag-list'),
    path('notice-rows', NoticeRowView.as_view(), name='notice-row-list'),
    path('notice-page', NoticePageView.as_view(), name='notice-page')
]