from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import CursorPagination

from .models import Project
from .serializers import ProjectSerializer


class ProjectCursorPagination(CursorPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created"


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProjectCursorPagination

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
