from django.urls import path

from .views import GitHubActivityListView

app_name = "activities"

urlpatterns = [
    path("", GitHubActivityListView.as_view(), name="activity-list"),
]
