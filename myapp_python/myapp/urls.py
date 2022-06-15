"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from sign import m3u8_text, mp4_text

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_data/', m3u8_text.detail.as_view()),
    path('get_m3u8/', mp4_text.get_m3u8.as_view()),
    path('requests_m3u8/', m3u8_text.requests_m3u8.as_view()),
]
