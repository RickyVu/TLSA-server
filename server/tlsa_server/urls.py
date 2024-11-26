"""
URL configuration for tlsa_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import RegisterView, LoginView, ValidateTokenView, RefreshTokenView, VerifyView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/v1/docs/redoc/', SpectacularRedocView.as_view(), name='redoc-ui'),
    
    # Authentication
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/token/validate/', ValidateTokenView.as_view(), name='validate_token'),
    path('api/v1/refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('api/v1/verify/', VerifyView.as_view(), name='verify'),

    # Apps
    path('api/v1/labs/', include('labs.urls')),
    path('api/v1/courses/', include('courses.urls')),
    path('api/v1/classes/', include('classes.urls')),
    path('api/v1/notices/', include('notices.urls'))
]

##swagger:   http://127.0.0.1:8000/api/v1/docs/swagger/