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

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity <= 0:
            raise forms.ValidationError(
                "Material quantity must be greater than 0."
            )

        return quantity