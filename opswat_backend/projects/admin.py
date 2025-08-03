from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "status", "start_date", "end_date", "created")
    list_filter = ("status", "created", "modified")
    search_fields = ("name", "description", "user__email")
    readonly_fields = ("created", "modified")
    list_select_related = ("user",)
