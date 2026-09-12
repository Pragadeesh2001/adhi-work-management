from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from projects.models import Project

from progress.forms import ProgressForm
from materials.forms import MaterialForm
from issues.forms import IssueForm

from progress.models import Progress
from materials.models import Material
from issues.models import Issue


@login_required
def team_leader_dashboard(request):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    projects = request.user.projects.all()

    return render(
        request,
        "projects/team_leader_dashboard.html",
        {
            "projects": projects
        }
    )


@login_required
def project_detail(request, project_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    project = get_object_or_404(
        Project,
        id=project_id,
        team_leader=request.user
    )

    progress_updates = project.progress_updates.all()
    materials = project.materials.all()
    issues = project.issues.all()
    workers = project.workers.all()

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "progress_updates": progress_updates,
            "materials": materials,
            "issues": issues,
            'workers':workers
        }
    )


@login_required
def add_progress(request, project_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    project = get_object_or_404(
        Project,
        id=project_id,
        team_leader=request.user
    )

    if request.method == "POST":

        form = ProgressForm(request.POST)

        if form.is_valid():

            progress = form.save(commit=False)
            progress.project = project
            progress.save()

            # Recalculate total progress
            total_completed = project.progress_updates.aggregate(
                total=Sum("completed_quantity")
            )["total"] or 0

            project.completed_quantity = total_completed

            # Update project status
            if total_completed >= project.planned_quantity:
                project.status = Project.Status.COMPLETED

            elif total_completed > 0:
                project.status = Project.Status.IN_PROGRESS

            else:
                project.status = Project.Status.NOT_STARTED

            project.save()

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:
        form = ProgressForm()

    return render(
        request,
        "projects/add_progress.html",
        {
            "project": project,
            "form": form,
        }
    )


@login_required
def edit_progress(request, progress_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    progress = get_object_or_404(
        Progress,
        id=progress_id,
        project__team_leader=request.user
    )

    if request.method == "POST":

        form = ProgressForm(
            request.POST,
            instance=progress
        )

        if form.is_valid():

            form.save()

            project = progress.project

            # Recalculate total progress
            total_completed = project.progress_updates.aggregate(
                total=Sum("completed_quantity")
            )["total"] or 0

            project.completed_quantity = total_completed

            # Update project status
            if total_completed >= project.planned_quantity:
                project.status = Project.Status.COMPLETED

            elif total_completed > 0:
                project.status = Project.Status.IN_PROGRESS

            else:
                project.status = Project.Status.NOT_STARTED

            project.save()

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:

        form = ProgressForm(
            instance=progress
        )

    return render(
        request,
        "projects/edit_progress.html",
        {
            "progress": progress,
            "project": progress.project,
            "form": form,
        }
    )


@login_required
def delete_progress(request, progress_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    progress = get_object_or_404(
        Progress,
        id=progress_id,
        project__team_leader=request.user
    )

    if request.method == "POST":

        project = progress.project

        # Delete progress record first
        progress.delete()

        # Recalculate total progress
        total_completed = project.progress_updates.aggregate(
            total=Sum("completed_quantity")
        )["total"] or 0

        project.completed_quantity = total_completed

        # Update project status
        if total_completed >= project.planned_quantity:
            project.status = Project.Status.COMPLETED

        elif total_completed > 0:
            project.status = Project.Status.IN_PROGRESS

        else:
            project.status = Project.Status.NOT_STARTED

        project.save()

        return redirect(
            "project_detail",
            project_id=project.id
        )

    return render(
        request,
        "projects/delete_progress.html",
        {
            "progress": progress,
            "project": progress.project,
        }
    )


@login_required
def add_material(request, project_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    project = get_object_or_404(
        Project,
        id=project_id,
        team_leader=request.user
    )

    if request.method == "POST":

        form = MaterialForm(request.POST)

        if form.is_valid():

            material = form.save(commit=False)
            material.project = project
            material.save()

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:

        form = MaterialForm()

    return render(
        request,
        "projects/add_material.html",
        {
            "project": project,
            "form": form,
        }
    )


@login_required
def edit_material(request, material_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    material = get_object_or_404(
        Material,
        id=material_id,
        project__team_leader=request.user
    )

    if request.method == "POST":

        form = MaterialForm(
            request.POST,
            instance=material
        )

        if form.is_valid():

            form.save()

            return redirect(
                "project_detail",
                project_id=material.project.id
            )

    else:

        form = MaterialForm(
            instance=material
        )

    return render(
        request,
        "projects/edit_material.html",
        {
            "material": material,
            "project": material.project,
            "form": form,
        }
    )


@login_required
def delete_material(request, material_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    material = get_object_or_404(
        Material,
        id=material_id,
        project__team_leader=request.user
    )

    if request.method == "POST":

        project_id = material.project.id

        material.delete()

        return redirect(
            "project_detail",
            project_id=project_id
        )

    return render(
        request,
        "projects/delete_material.html",
        {
            "material": material,
            "project": material.project,
        }
    )


@login_required
def add_issue(request, project_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    project = get_object_or_404(
        Project,
        id=project_id,
        team_leader=request.user
    )

    if request.method == "POST":

        form = IssueForm(request.POST)

        if form.is_valid():

            issue = form.save(commit=False)
            issue.project = project
            issue.save()

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:

        form = IssueForm()

    return render(
        request,
        "projects/add_issue.html",
        {
            "project": project,
            "form": form,
        }
    )


@login_required
def edit_issue(request, issue_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    issue = get_object_or_404(
        Issue,
        id=issue_id,
        project__team_leader=request.user
    )

    if request.method == "POST":

        form = IssueForm(
            request.POST,
            instance=issue
        )

        if form.is_valid():

            form.save()

            return redirect(
                "project_detail",
                project_id=issue.project.id
            )

    else:

        form = IssueForm(
            instance=issue
        )

    return render(
        request,
        "projects/edit_issue.html",
        {
            "issue": issue,
            "project": issue.project,
            "form": form,
        }
    )


@login_required
def delete_issue(request, issue_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    issue = get_object_or_404(
        Issue,
        id=issue_id,
        project__team_leader=request.user
    )

    if request.method == "POST":

        project_id = issue.project.id

        issue.delete()

        return redirect(
            "project_detail",
            project_id=project_id
        )

    return render(
        request,
        "projects/delete_issue.html",
        {
            "issue": issue,
            "project": issue.project,
        }
    )