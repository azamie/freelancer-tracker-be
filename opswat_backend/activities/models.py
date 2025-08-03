from django.db import models
from model_utils.models import TimeStampedModel
from projects.models import Project


class Repository(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="repositories",
    )
    repo_name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        app_label = "activities"
        ordering = ["-created"]
        verbose_name_plural = "repositories"

    def __str__(self):
        return f"{self.project.name} - {self.repo_name}"


class GitHubActivity(TimeStampedModel):
    class ActivityType(models.TextChoices):
        PUSH_COMMITS = "push_commits", "Push Commits"
        CREATE_PR = "create_pr", "Create Pull Request"
        MERGE_PR = "merge_pr", "Merge Pull Request"
        CREATE_RELEASE = "create_release", "Create Release"

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="github_activities",
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
    )
    details = models.JSONField(default=dict)
    username = models.CharField(max_length=100)

    class Meta:
        app_label = "activities"
        ordering = ["-created"]
        verbose_name_plural = "GitHub activities"

    def __str__(self):
        return (
            f"{self.repository.repo_name} - "
            f"{self.get_activity_type_display()} by {self.username}"
        )
