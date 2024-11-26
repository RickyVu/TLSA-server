from django.urls import path
from .views import LabView, LabManagerView

urlpatterns = [
    path('lab', LabView.as_view(), name='lab'),
    path('managers', LabManagerView.as_view(), name='lab-manager')
]