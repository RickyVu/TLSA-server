from django.urls import path
from .views import LabView

urlpatterns = [
    path('', LabView.as_view(), name='manage-lab'),
]