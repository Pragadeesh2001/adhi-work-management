from django.test import TestCase

from .forms import ProgressForm


class ProgressFormTest(TestCase):

    def test_completed_quantity_must_be_positive(self):
        form = ProgressForm(
            data={
                "date": "2026-09-24",
                "completed_quantity": 0,
                "remarks": "Test progress",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("completed_quantity", form.errors)

    def test_positive_completed_quantity_is_valid(self):
        form = ProgressForm(
            data={
                "date": "2026-09-24",
                "completed_quantity": 10,
                "remarks": "Test progress",
            }
        )

        self.assertTrue(form.is_valid())