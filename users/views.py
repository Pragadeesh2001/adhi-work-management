from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from .models import User
from projects.models import Project
from issues.models import Issue
from django.db.models import Sum
from projects.forms import ProjectAssignmentForm, ProjectStatusForm,ProjectForm
from django.contrib.auth import authenticate, login
def login_view(request):

    if request.user.is_authenticated:

        if request.user.role == "MANAGEMENT":
            return redirect("management_dashboard")

        elif request.user.role == "TEAM_LEADER":
            return redirect("team_leader_dashboard")

    if request.method == "POST":

        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "MANAGEMENT":
                return redirect("management_dashboard")

            elif user.role == "TEAM_LEADER":
                return redirect("team_leader_dashboard")

        else:
            return render(
                request,
                "registration/login.html",
                {
                    "error": "Invalid email or password."
                }
            )

    return render(
        request,
        "registration/login.html"
    )

@login_required
def management_dashboard(request):

    if request.user.role != "MANAGEMENT":
        return render(
            request,
            "users/access_denied.html"
        )

    team_leaders = User.objects.filter(
        role=User.Role.TEAM_LEADER
    )

    status = request.GET.get("status")

    if status:
        team_leaders = team_leaders.prefetch_related(
            Prefetch(
                "projects",
                queryset=Project.objects.filter(status=status)
            )
        )
    else:
        team_leaders = team_leaders.prefetch_related("projects")

    total_team_leaders = User.objects.filter(
        role=User.Role.TEAM_LEADER
    ).count()

    total_projects = Project.objects.count()
    all_projects = Project.objects.select_related(
    "team_leader",
    "tender"
)

    if status:
        all_projects = all_projects.filter(
            status=status
        )

    all_projects = all_projects.order_by("-created_at")
    completed_projects = Project.objects.filter(
        status=Project.Status.COMPLETED
    ).count()

    in_progress_projects = Project.objects.filter(
        status=Project.Status.IN_PROGRESS
    ).count()

    not_started_projects = Project.objects.filter(
        status=Project.Status.NOT_STARTED
    ).count()

    on_hold_projects = Project.objects.filter(
        status=Project.Status.ON_HOLD
    ).count()

    unassigned_projects = Project.objects.filter(
        team_leader__isnull=True
    ).count()

    open_issues = Issue.objects.filter(
        status="OPEN"
    ).count()

    return render(
        request,
        "users/management_dashboard.html",
        {
            "team_leaders": team_leaders,
            "total_team_leaders": total_team_leaders,
            "total_projects": total_projects,
            "completed_projects": completed_projects,
            "in_progress_projects": in_progress_projects,
            "not_started_projects": not_started_projects,
            "on_hold_projects": on_hold_projects,
            "unassigned_projects": unassigned_projects,
            "open_issues": open_issues,
            "selected_status": status,
            "all_projects": all_projects,
        }
    )
@login_required
def management_team_leader(request, user_id):

    if request.user.role != "MANAGEMENT":
        return render(
            request,
            "users/access_denied.html"
        )

    team_leader = get_object_or_404(
        User,
        id=user_id,
        role=User.Role.TEAM_LEADER
    )

    projects = team_leader.projects.all()

    return render(
        request,
        "users/management_team_leader.html",
        {
            "team_leader": team_leader,
            "projects": projects,
        }
    )

@login_required
def management_project_detail(request, project_id):

    if request.user.role != "MANAGEMENT":
        return render(
            request,
            "users/access_denied.html"
        )

    project = get_object_or_404(
        Project,
        id=project_id
    )

    progress_updates = project.progress_updates.all()
    materials = project.materials.all()
    issues = project.issues.all()
    open_issues = issues.filter(status="OPEN").count()
    in_progress_issues = issues.filter(status="IN_PROGRESS").count()
    resolved_issues = issues.filter(status="RESOLVED").count()

    renaining_quantity = project.planned_quantity-project.completed_quantity
    if project.planned_quantity > 0:
        completion_percentage = (
            project.completed_quantity / project.planned_quantity) * 100
    else:
        completion_percentage = 0
        
    total_progress_quantity = progress_updates.aggregate(
    total=Sum("completed_quantity")
    )["total"] or 0

    return render(
        request,
        "users/management_project_detail.html",
        {
            "project": project,
            "progress_updates": progress_updates,
            "materials": materials,
            "issues": issues,
            "remaining_quantity":renaining_quantity,
            "completion_percentage":completion_percentage,
            "total_progress_quantity":total_progress_quantity,
            "open_issues": open_issues,
            "in_progress_issues": in_progress_issues,
            "resolved_issues": resolved_issues,
        }
    )

@login_required
def assign_project(request, project_id):

    if request.user.role != "MANAGEMENT":
        return render(
            request,
            "users/access_denied.html"
        )

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        form = ProjectAssignmentForm(
            request.POST,
            instance=project
        )

        if form.is_valid():
            form.save()

            return redirect(
                "management_project_detail",
                project_id=project.id
            )

    else:

        form = ProjectAssignmentForm(
            instance=project
        )

    return render(
        request,
        "users/assign_project.html",
        {
            "project": project,
            "form": form,
        }
    )

@login_required
def change_project_status(request, project_id):

    if request.user.role != "MANAGEMENT":
        return render(
            request,
            "users/access_denied.html"
        )

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        form = ProjectStatusForm(
            request.POST,
            instance=project
        )

        if form.is_valid():
            form.save()

            return redirect(
                "management_project_detail",
                project_id=project.id
            )

    else:

        form = ProjectStatusForm(
            instance=project
        )

    return render(
        request,
        "users/change_project_status.html",
        {
            "project": project,
            "form": form,
        }
    )

@login_required
def create_project(request):

    if request.user.role != "MANAGEMENT":
        return render(
            request,
            "users/access_denied.html"
        )

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "management_dashboard"
            )

    else:

        form = ProjectForm()

    return render(
        request,
        "users/create_project.html",
        {
            "form": form
        }
    )