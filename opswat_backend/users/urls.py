from django.urls import path

from .views import UserDetailsView

app_name = "users"
urlpatterns = [
    path("me/", UserDetailsView.as_view(), name="user-detail"),
]
