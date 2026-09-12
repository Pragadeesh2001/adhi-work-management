from django.db import models
from projects.models import Project


class Issue(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("OPEN", "Open"),
            ("IN_PROGRESS", "In Progress"),
            ("RESOLVED", "Resolved"),
        ],
        default="OPEN"
    )

    def __str__(self):
        return f"{self.title} - {self.project.project_number}"