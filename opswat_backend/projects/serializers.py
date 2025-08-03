from rest_framework import serializers

from .models import Invoice
from .models import Project
from .models import Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "status",
            "start_date",
            "end_date",
            "created",
            "modified",
        ]
        read_only_fields = ["id", "created", "modified"]


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "task_type",
            "status",
            "description",
            "project_name",
            "created",
            "modified",
        ]
        read_only_fields = ["id", "created", "modified", "project_name"]


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "amount",
            "status",
            "due_date",
            "project_name",
            "created",
            "modified",
        ]
        read_only_fields = [
            "id",
            "invoice_number",
            "created",
            "modified",
            "project_name",
        ]
