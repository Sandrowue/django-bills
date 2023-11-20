import django.contrib.auth.urls
from django.urls import include, path

urlpatterns = [
    path("", include(django.contrib.auth.urls)),
]