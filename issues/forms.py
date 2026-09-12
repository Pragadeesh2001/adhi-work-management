from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue

        fields = [
            "title",
            "description",
            "date",
            "status",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }