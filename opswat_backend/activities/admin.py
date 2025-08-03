from django.contrib import admin

from .models import GitHubActivity
from .models import Repository


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("repo_name", "project", "url")
    list_filter = ("project",)
    search_fields = ("repo_name", "url")


@admin.register(GitHubActivity)
class GitHubActivityAdmin(admin.ModelAdmin):
    list_display = ("repository", "activity_type", "username", "created")
    list_filter = ("activity_type", "created")
    search_fields = ("username", "repository__repo_name")
    readonly_fields = ("created", "modified")
