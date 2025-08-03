from rest_framework import serializers

from .models import GitHubActivity


class GitHubActivitySerializer(serializers.ModelSerializer):
    repository_name = serializers.CharField(
        source="repository.repo_name",
        read_only=True,
    )
    project_name = serializers.CharField(
        source="repository.project.name",
        read_only=True,
    )

    class Meta:
        model = GitHubActivity
        fields = [
            "id",
            "repository",
            "repository_name",
            "project_name",
            "activity_type",
            "details",
            "username",
            "created",
            "modified",
        ]
