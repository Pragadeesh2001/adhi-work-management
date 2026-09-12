from django.urls import path
from .views import team_leader_dashboard,project_detail,add_progress, add_material, add_issue,edit_progress,delete_progress,edit_material,delete_material,edit_issue,delete_issue


urlpatterns = [
    path(
        "team-leader/",
        team_leader_dashboard,
        name="team_leader_dashboard"
    ),

    path(
        "project/<int:project_id>/",
        project_detail,
        name="project_detail"
    ),
    path(
        "project/<int:project_id>/add-progress",
        add_progress,
        name="add_progress"
    ),
    path(
    "project/<int:project_id>/add-material/",
    add_material,
    name="add_material"
    ),
    path(
    "project/<int:project_id>/add-issue/",
    add_issue,
    name="add_issue"
    ),
    path("project/<int:progress_id>/edit/",
        edit_progress,
        name="edit_progress"),
    path(
    "progress/<int:progress_id>/delete/",
    delete_progress,
    name="delete_progress"
    ),
    path(
    "material/<int:material_id>/edit/",
    edit_material,
    name="edit_material"
    ),
    path(
    "material/<int:material_id>/delete/",
    delete_material,
    name="delete_material"
    ),
    path(
    "issue/<int:issue_id>/edit/",
    edit_issue,
    name="edit_issue"
    ),
    path(
    "issue/<int:issue_id>/delete/",
    delete_issue,
    name="delete_issue"
    ),
]