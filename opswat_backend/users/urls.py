from django.urls import path

from .views import UserDetailsView
from .views import UserSummaryView

app_name = "users"
urlpatterns = [
    path("me/", UserDetailsView.as_view(), name="user-detail"),
    path("me/summary/", UserSummaryView.as_view(), name="user-summary"),
]
