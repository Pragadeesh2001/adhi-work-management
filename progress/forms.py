from django import forms

from .models import Progress


class ProgressForm(forms.ModelForm):

    class Meta:
        model = Progress
        fields = [
            "date",
            "completed_quantity",
            "remarks",
        ]

    def clean_completed_quantity(self):
        quantity = self.cleaned_data["completed_quantity"]

        if quantity <= 0:
            raise forms.ValidationError(
                "Completed quantity must be greater than 0."
            )

        return quantity
    