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