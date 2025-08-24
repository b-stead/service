from django.urls import path
from .views import OAuthLoginView

urlpatterns = [
    path("login/", OAuthLoginView.as_view(), name="oauth_login"),
]
