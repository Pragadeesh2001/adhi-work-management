from django.test import TestCase

from .forms import WorkerForm


class WorkerFormTest(TestCase):

    def test_name_is_required(self):
        form = WorkerForm(
            data={
                "name": "",
                "phone": "9876543210",
                "role": "Mason",
                "is_active": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_valid_worker_is_accepted(self):
        form = WorkerForm(
            data={
                "name": "Ramesh",
                "phone": "9876543210",
                "role": "Mason",
                "is_active": True,
            }
        )

        self.assertTrue(form.is_valid())