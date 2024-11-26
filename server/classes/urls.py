from django.urls import path
from .views import ClassView

urlpatterns = [
    path('class/', ClassView.as_view(), name='class'),
]