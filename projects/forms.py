from django import forms
from users.models import User
from .models import Project


class ProjectAssignmentForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["team_leader"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["team_leader"].queryset = User.objects.filter(
            role=User.Role.TEAM_LEADER
        )

class ProjectStatusForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["status"]

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            "project_number",
            "name",
            "tender",
            "description",
            "team_leader",
            "planned_quantity",
            "unit",
            "start_date",
            "end_date",
            "status",
        ]

        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["team_leader"].queryset = User.objects.filter(
            role=User.Role.TEAM_LEADER
        )
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        planned_quantity = cleaned_data.get("planned_quantity")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    "End date cannot be before start date."
                )

        if planned_quantity is not None:
            if planned_quantity <= 0:
                raise forms.ValidationError(
                    "Planned quantity must be greater than 0."
                )

        return cleaned_data
