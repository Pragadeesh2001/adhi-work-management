from django.contrib import admin
from .models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "phone",
        "role",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "role",
    )

    search_fields = (
        "name",
        "phone",
        "project__project_number",
    )