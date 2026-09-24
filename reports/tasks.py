from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from projects.models import Project
from progress.models import Progress
from materials.models import Material
from issues.models import Issue
from workers.models import Worker


@shared_task
def generate_daily_report():
    today = timezone.localdate()

    projects = Project.objects.all()
    today_progress = Progress.objects.filter(date=today)
    today_materials = Material.objects.filter(date=today)
    today_issues = Issue.objects.filter(date=today)
    active_workers = Worker.objects.filter(is_active=True)

    project_details = ""

    for project in projects:
        project_details += f"""
Project Number: {project.project_number}
Project Name: {project.name}
Status: {project.status}
Planned Quantity: {project.planned_quantity} {project.unit}
Completed Quantity: {project.completed_quantity} {project.unit}
----------------------------------------
"""

    progress_details = ""

    for progress in today_progress:
        progress_details += f"""
Project: {progress.project.name}
Completed Quantity: {progress.completed_quantity} {progress.project.unit}
Remarks: {progress.remarks}
----------------------------------------
"""
    material_details = ""

    for material in today_materials:
        material_details += f"""
Project: {material.project.name}
Material: {material.name}
Quantity: {material.quantity} {material.unit}
Remarks: {material.remarks}
----------------------------------------
"""
    issue_details = ""

    for issue in today_issues:
        issue_details += f"""
Project: {issue.project.name}
Issue: {issue.title}
Description: {issue.description}
Status: {issue.status}
----------------------------------------
"""
    worker_details = ""

    for worker in active_workers:
        worker_details += f"""
Project: {worker.project.name}
Worker Name: {worker.name}
Role: {worker.role}
Phone: {worker.phone}
----------------------------------------
"""
    report = f"""
ADHI ENTERPRISES - DAILY WORK REPORT

Date: {today}

SUMMARY
-------
Total Projects: {projects.count()}
Today's Progress Entries: {today_progress.count()}
Today's Material Entries: {today_materials.count()}
Today's Issues: {today_issues.count()}
Active Workers: {active_workers.count()}


PROJECT DETAILS
---------------
{project_details}


TODAY'S PROGRESS
----------------
{progress_details}

TODAY'S MATERIALS
-----------------
{material_details}
TODAY'S ISSUES
--------------
{issue_details}
ACTIVE WORKERS
--------------
{worker_details}

This is an automatically generated daily report.
"""

    send_mail(
        subject=f"Adhi Enterprises - Daily Work Report - {today}",
        message=report,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.MANAGEMENT_EMAIL],
    )

    print("\n========== DAILY WORK REPORT ==========")
    print(report)
    print("Email sent successfully.")
    print("=======================================\n")

    return "Daily report generated and emailed successfully"

