from django.db import models
from projects.models import Project


class Material(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="materials"
    )

    name = models.CharField(
        max_length=200
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=50
    )

    date = models.DateField()

    remarks = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.project.project_number}"