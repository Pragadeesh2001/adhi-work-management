from django.test import TestCase

from .forms import MaterialForm


class MaterialFormTest(TestCase):

    def test_quantity_must_be_positive(self):
        form = MaterialForm(
            data={
                "name": "Cement",
                "quantity": 0,
                "unit": "bags",
                "date": "2026-09-24",
                "remarks": "Test material",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)

    def test_positive_quantity_is_valid(self):
        form = MaterialForm(
            data={
                "name": "Cement",
                "quantity": 10,
                "unit": "bags",
                "date": "2026-09-24",
                "remarks": "Test material",
            }
        )

        self.assertTrue(form.is_valid())