from django.urls import path
from .views import (ClassView,
                    TeacherClassView,
                    ClassLocationView,
                    CommentToClassView,
                    ExperimentView)

urlpatterns = [
    path('class', ClassView.as_view(), name='class'),
    path('teachers', TeacherClassView.as_view(), name='teach-class'),
    path('locations', ClassLocationView.as_view(), name='class-location'),
    path('comments', CommentToClassView.as_view(), name='class-comments'),
    path('experiments/', ExperimentView.as_view(), name='experiment-list'),
]
