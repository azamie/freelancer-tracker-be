from datetime import timedelta

from activities.models import GitHubActivity
from django.db.models import Sum
from django.utils import timezone
from projects.models import Invoice
from projects.models import Project
from projects.models import Task
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserSummarySerializer(serializers.Serializer):
    active_projects = serializers.SerializerMethodField()
    pending_tasks = serializers.SerializerMethodField()
    monthly_revenue = serializers.SerializerMethodField()
    weekly_github_releases = serializers.SerializerMethodField()

    def get_active_projects(self, obj):
        return Project.objects.filter(
            user=obj, status=Project.Status.IN_PROGRESS,
        ).count()

    def get_pending_tasks(self, obj):
        return Task.objects.filter(
            project__user=obj,
            status__in=[
                Task.Status.UNSTARTED,
                Task.Status.IN_PROGRESS,
                Task.Status.REJECTED,
            ],
        ).count()

    def get_monthly_revenue(self, obj):
        thirty_days_ago = timezone.now() - timedelta(days=30)

        result = Invoice.objects.filter(
            project__user=obj, status=Invoice.Status.PAID, created__gte=thirty_days_ago,
        ).aggregate(total=Sum("amount"))

        return result["total"] or 0

    def get_weekly_github_releases(self, obj):
        seven_days_ago = timezone.now() - timedelta(days=7)

        return GitHubActivity.objects.filter(
            repository__project__user=obj,
            activity_type=GitHubActivity.ActivityType.CREATE_RELEASE,
            created__gte=seven_days_ago,
        ).count()
