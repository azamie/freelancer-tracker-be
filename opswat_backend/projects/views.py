from django.db import models
from django.db.models import Count
from django.db.models import Sum
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import CursorPagination

from .models import Invoice
from .models import Project
from .models import Task
from .serializers import InvoiceSerializer
from .serializers import ProjectSerializer
from .serializers import TaskSerializer


class ProjectCursorPagination(CursorPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created"


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProjectCursorPagination

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class TaskCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created"


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TaskCursorPagination

    def get_queryset(self):
        queryset = Task.objects.select_related("project").filter(
            project__user=self.request.user,
        )

        project_ids = self.request.query_params.getlist("projects[]")
        if project_ids:
            queryset = queryset.filter(project__id__in=project_ids)

        return queryset


class InvoiceCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created"


class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = InvoiceCursorPagination

    def get_queryset(self):
        return Invoice.objects.select_related("project").filter(
            project__user=self.request.user,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Calculate aggregated values
        aggregates = queryset.aggregate(
            total_paid=Sum("amount", filter=models.Q(status="PAID")),
            total_overdue=Sum("amount", filter=models.Q(status="OVERDUE")),
            total_invoices=Count("id"),
        )

        # Get paginated response
        response = super().list(request, *args, **kwargs)

        # Add aggregated data to response
        response.data["totalPaid"] = aggregates["total_paid"] or 0
        response.data["totalOverdue"] = aggregates["total_overdue"] or 0
        response.data["totalInvoices"] = aggregates["total_invoices"]

        return response
