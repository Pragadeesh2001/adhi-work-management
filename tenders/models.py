from django.db import models
from customers.models import Customer


class Tender(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    tender_number = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=200
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="tenders"
    )

    description = models.TextField(
        blank=True
    )

    contract_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    start_date = models.DateField()

    end_date = models.DateField()

    location = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.tender_number} - {self.name}"