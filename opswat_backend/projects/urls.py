from django.urls import path

from .views import ProjectListView
from .views import TaskListView

app_name = "projects"

urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]
