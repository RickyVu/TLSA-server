from django.urls import path
<<<<<<< HEAD
from .views import (ClassView,
                    TeacherClassView,
                    ClassLocationView,
                    CommentToClassView)
=======
from .views import (ClassView, 
                    TeacherClassView, 
                    ClassLocationView, 
                    CommentToClassView,
                    ExperimentView)
>>>>>>> tlsa/dev-ricky

urlpatterns = [
    path('class', ClassView.as_view(), name='class'),
    path('teachers', TeacherClassView.as_view(), name='teach-class'),
    path('locations', ClassLocationView.as_view(), name='class-location'),
    path('comments', CommentToClassView.as_view(), name='class-comments'),
<<<<<<< HEAD
]
=======
    path('experiments/', ExperimentView.as_view(), name='experiment-list'),
]
>>>>>>> tlsa/dev-ricky
