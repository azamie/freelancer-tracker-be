from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import CursorPagination

from .models import GitHubActivity
from .serializers import GitHubActivitySerializer


class GitHubActivityCursorPagination(CursorPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created"


class GitHubActivityListView(generics.ListAPIView):
    serializer_class = GitHubActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GitHubActivityCursorPagination

    def get_queryset(self):
        return GitHubActivity.objects.select_related(
            "repository",
            "repository__project",
        ).filter(
            repository__project__user=self.request.user,
        )
