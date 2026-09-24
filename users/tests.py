from django.test import TestCase
from django.urls import reverse

from .models import User


class RoleAccessTest(TestCase):

    def test_management_can_access_dashboard(self):
        user = User.objects.create_user(
            email="management@test.com",
            password="testpassword",
            role=User.Role.MANAGEMENT,
        )

        self.client.login(
            email="management@test.com",
            password="testpassword",
        )

        response = self.client.get(
            reverse("management_dashboard")
        )

        self.assertEqual(response.status_code, 200)

    def test_team_leader_cannot_access_management_dashboard(self):
        user = User.objects.create_user(
            email="leader@test.com",
            password="testpassword",
            role=User.Role.TEAM_LEADER,
        )

        self.client.login(
            email="leader@test.com",
            password="testpassword",
        )

        response = self.client.get(
            reverse("management_dashboard")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "users/access_denied.html"
        )