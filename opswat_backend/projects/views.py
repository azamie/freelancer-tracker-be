from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import CursorPagination

from .models import Project
from .models import Task
from .serializers import ProjectSerializer
from .serializers import TaskSerializer


class ProjectCursorPagination(CursorPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created"


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProjectCursorPagination

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class TaskCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created"


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TaskCursorPagination

    def get_queryset(self):
        queryset = Task.objects.select_related("project").filter(
            project__user=self.request.user,
        )

        project_ids = self.request.query_params.getlist("projects[]")
        if project_ids:
            queryset = queryset.filter(project__id__in=project_ids)

        return queryset
