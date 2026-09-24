from django.test import TestCase

from .forms import IssueForm


class IssueFormTest(TestCase):

    def test_title_is_required(self):
        form = IssueForm(
            data={
                "title": "",
                "description": "Test issue",
                "date": "2026-09-24",
                "status": "OPEN",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_valid_issue_is_accepted(self):
        form = IssueForm(
            data={
                "title": "Material shortage",
                "description": "Cement stock is low.",
                "date": "2026-09-24",
                "status": "OPEN",
            }
        )

        self.assertTrue(form.is_valid())