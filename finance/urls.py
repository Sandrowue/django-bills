from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name="index"),
    path("tilit/", views.AccountList.as_view(), name="accounts"),
    path("tilit/<int:pk>/",
         views.AccountDetail.as_view(),
         name="account-detail",
         ),
    path("dokumentit/", views.DocumentList.as_view(), name="documents"),
    path(
        "dokumentit/<int:pk>/",
        views.DocumentDetail.as_view(),
        name="document-detail"
    ),
    path("kategoriat/", views.CategoryList.as_view(), name="categories"),
    path(
        "kategoriat/<int:pk>/",
        views.CategoryDetail.as_view(),
        name="category-detail",
    ),  
]