from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from projects.models import Project
from .forms import WorkerForm
from .forms import Worker

@login_required
def add_worker(request, project_id):

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

        form = WorkerForm(request.POST)

        if form.is_valid():

            worker = form.save(commit=False)
            worker.project = project
            worker.save()

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:

        form = WorkerForm()

    return render(
        request,
        "workers/add_worker.html",
        {
            "project": project,
            "form": form,
        }
    )

@login_required
def edit_worker(request, worker_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    worker = get_object_or_404(
        Worker,
        id=worker_id,
        project__team_leader=request.user
    )

    if request.method == "POST":

        form = WorkerForm(
            request.POST,
            instance=worker
        )

        if form.is_valid():

            form.save()

            return redirect(
                "project_detail",
                project_id=worker.project.id
            )

    else:

        form = WorkerForm(
            instance=worker
        )

    return render(
        request,
        "workers/edit_worker.html",
        {
            "worker": worker,
            "project": worker.project,
            "form": form,
        }
    )
@login_required
def delete_worker(request, worker_id):

    if request.user.role != "TEAM_LEADER":
        return render(
            request,
            "users/access_denied.html"
        )

    worker = get_object_or_404(
        Worker,
        id=worker_id,
        project__team_leader=request.user
    )

    project_id = worker.project.id

    if request.method == "POST":
        worker.delete()

        return redirect(
            "project_detail",
            project_id=project_id
        )

    return render(
        request,
        "workers/delete_worker.html",
        {
            "worker": worker,
            "project": worker.project,
        }
    )