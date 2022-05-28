from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.CryptoView.as_view(), name="crypto_view"),
    path(r"<str:platform>", views.CryptoView.as_view(), name="crypto_view"),
]
