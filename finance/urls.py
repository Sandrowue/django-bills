from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name="index"),
    path("tilit/", views.accounts, name="accounts"),
    path("dokumentit/", views.documents, name="documents")   
]