"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from equipment.auth_views import RegisterView, LoginView, LogoutView, UserInfoView
from equipment.api_root_view import APIRootView

urlpatterns = [
    # API Root - Shows available endpoints
    path('', APIRootView.as_view(), name='api-root'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Equipment API Endpoints (prefixed with /api/)
    # - POST /api/upload/
    # - GET /api/datasets/
    # - GET /api/datasets/<id>/
    # - GET /api/datasets/<id>/summary/
    # - GET /api/datasets/<id>/report/pdf/
    path('api/', include('equipment.urls')),
    
    # Authentication Endpoints
    # POST /api/auth/register/ - User registration
    path('api/auth/register/', RegisterView.as_view(), name='auth-register'),
    
    # POST /api/auth/login/ - User login (returns token)
    path('api/auth/login/', LoginView.as_view(), name='auth-login'),
    
    # POST /api/auth/logout/ - User logout (invalidates token)
    path('api/auth/logout/', LogoutView.as_view(), name='auth-logout'),
    
    # GET /api/auth/user/ - Get current user info
    path('api/auth/user/', UserInfoView.as_view(), name='auth-user'),
]
