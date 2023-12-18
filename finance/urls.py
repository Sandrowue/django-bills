from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name="index"),
    path("tilit/", views.AccountList.as_view(), name="accounts"),
    path("tilit/<int:pk>/",
         views.AccountDetail.as_view(),
         name="account-detail",
         ),
    path(
        "tilit/poista/<int:pk>/",
        views.AccountDelete.as_view(),
        name="account-delete",
    ),
    path(
        "tilit/uusi/",
        views.AccountCreate.as_view(),
        name="account-new",
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
    path(
        "kategoriat/poista/<int:pk>/",
        views.CategoryDelete.as_view(),
        name="category-delete",
    ), 
    path(
        "kategoriat/uusi/",
        views.CategoryCreate.as_view(),
        name="category-new",
    ),
    path(
        "kategoriat/luo-oletuskategoriat/",
        views.CreateDefaultCategoriesFormView.as_view(),
        name="category-create-defaults",
    ),
    # Tilitapatuman luonnissa käytetään account_id:tä, jotta tilitapahtuma luodaan ko. tilille
    path(
        "tilit/<int:account_id>/uusi-tilitapahtuma/",
        views.TransactionCreate.as_view(),
        name="transaction-new",
    ),
]