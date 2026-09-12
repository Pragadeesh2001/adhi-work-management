from django.db import models
from tenders.models import Tender
from users.models import User

class Project(models.Model):

    class Status(models.TextChoices):
        NOT_STARTED = "NOT_STARTED", "Not Started"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        ON_HOLD = "ON_HOLD", "On Hold"

    project_number = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=200
    )

    tender = models.ForeignKey(
        Tender,
        on_delete=models.PROTECT,
        related_name="projects"
    )

    description = models.TextField(
        blank=True
    )

    team_leader = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name="projects",
    null=True,
    blank=True
    )

    planned_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    completed_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    unit = models.CharField(
        max_length=50
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.NOT_STARTED
)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.project_number} - {self.name}"