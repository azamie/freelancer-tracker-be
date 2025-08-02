from django.urls import path

from .views import LoginAPIView
from .views import LogoutAPIView
from .views import RefreshTokenAPIView

app_name = "authentication"
urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
]
