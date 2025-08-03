from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Project(TimeStampedModel):
    class Status(models.TextChoices):
        UNSTARTED = "UNSTARTED", "Unstarted"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNSTARTED,
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "projects"
        ordering = ["-created"]

    def __str__(self):
        return self.name
