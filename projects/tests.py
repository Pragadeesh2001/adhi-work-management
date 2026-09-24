from django.test import TestCase
from django.urls import reverse

from users.models import User
from projects.models import Project
from tenders.models import Tender
from customers.models import Customer


class ProjectAccessTest(TestCase):

    def test_team_leader_cannot_access_another_leaders_project(self):
        leader1 = User.objects.create_user(
            email="leader1@test.com",
            password="testpassword",
            role=User.Role.TEAM_LEADER,
        )

        leader2 = User.objects.create_user(
            email="leader2@test.com",
            password="testpassword",
            role=User.Role.TEAM_LEADER,
        )

        customer = Customer.objects.create(
            name="Test Customer"
        )

        tender = Tender.objects.create(
            tender_number="TENDER-TEST-001",
            name="Test Tender",
            customer=customer,
            contract_amount=100000,
            start_date="2026-09-01",
            end_date="2026-09-30",
            location="Chennai",
            status=Tender.Status.ACTIVE,
        )

        project = Project.objects.create(
            project_number="TEST-001",
            name="Test Project",
            tender=tender,
            team_leader=leader2,
            planned_quantity=100,
            completed_quantity=0,
            unit="units",
            start_date="2026-09-01",
            end_date="2026-09-30",
            status=Project.Status.NOT_STARTED,
        )

        self.client.login(
            email="leader1@test.com",
            password="testpassword",
        )

        response = self.client.get(
            reverse(
                "project_detail",
                args=[project.id]
            )
        )

        self.assertEqual(response.status_code, 404)