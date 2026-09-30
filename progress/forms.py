from django import forms
from django.db.models import Sum
from .models import Progress


class ProgressForm(forms.ModelForm):

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

    class Meta:
        model = Progress
        fields = [
            "date",
            "completed_quantity",
            "remarks",
        ]

    def clean_date(self):
        date = self.cleaned_data["date"]

        if self.project:
            if date < self.project.start_date or date > self.project.end_date:
                raise forms.ValidationError(
                    f"Progress date must be between "
                    f"{self.project.start_date} and {self.project.end_date}."
                )

        return date

    def clean_completed_quantity(self):
        quantity = self.cleaned_data["completed_quantity"]

        if quantity <= 0:
            raise forms.ValidationError(
                "Completed quantity must be greater than 0."
            )

        if self.project:
            existing_total = self.project.progress_updates.aggregate(
                total=Sum("completed_quantity")
            )["total"] or 0

            # When editing an existing progress record,
            # don't count that same record twice.
            if self.instance and self.instance.pk:
                existing_total -= self.instance.completed_quantity

            new_total = existing_total + quantity

            if new_total > self.project.planned_quantity:
                raise forms.ValidationError(
                    f"Total completed quantity cannot be greater than "
                    f"planned quantity ({self.project.planned_quantity}). "
                    f"Current total after this entry would be {new_total}."
                )

        return quantity