"""config URL Configuration

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
from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.views.decorators.cache import cache_page

# Cache time to live is 15 minutes for each view.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<str:category>', cache_page(60*60*3)(views.newsList.as_view()), name="api"),
]

handler404 = views.error404.as_view()
