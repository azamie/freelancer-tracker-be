from django.contrib import admin

from .models import Invoice
from .models import Project
from .models import Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "status", "start_date", "end_date", "created")
    list_filter = ("status", "created", "modified")
    search_fields = ("name", "description", "user__email")
    readonly_fields = ("created", "modified")
    list_select_related = ("user",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "task_type", "status", "created")
    list_filter = ("task_type", "status", "created", "modified")
    search_fields = ("name", "description", "project__name")
    readonly_fields = ("created", "modified")
    list_select_related = ("project", "project__user")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "project",
        "amount",
        "status",
        "due_date",
        "created",
    )
    list_filter = ("status", "created", "modified", "due_date")
    search_fields = ("project__name", "amount")
    readonly_fields = ("created", "modified", "invoice_number")
    list_select_related = ("project",)
