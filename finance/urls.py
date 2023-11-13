from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name="index"),
    path("tilit/", views.AccountsList.as_view, name="accounts"),
    path("tilit/<int:pk>/",
         views.AccountDetail.as_view(),
         name="account-detail",
         ),
    path("dokumentit/", views.documents, name="documents"),   
]