from django.db import models
from projects.models import Project


class Worker(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="workers"
    )

    name = models.CharField(max_length=150)

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    role = models.CharField(
        max_length=100,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.project.project_number}"