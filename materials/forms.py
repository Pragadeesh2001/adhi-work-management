from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material

        fields = [
            "name",
            "quantity",
            "unit",
            "date",
            "remarks",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }