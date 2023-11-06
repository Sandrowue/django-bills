from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', include(finance.urls)),
    path('anmin/', admin.site.urls)
]