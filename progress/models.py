from django.db import models
from projects.models import Project


class Progress(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="progress_updates"
    )

    date = models.DateField()

    completed_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.project.project_number} - {self.date}"