"""matchpredictor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views

from games import views as games_views
from matchpredictor import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', games_views.ListGameView.as_view(), name='home'),
    path('', include('social_django.urls')),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('accounts/', include('allauth.urls')),
    path('clubs/', include('clubs.urls'), name='clubs'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
