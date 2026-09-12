from django.urls import path

from .views import (
    management_dashboard,
    management_team_leader,
    management_project_detail,
    assign_project,
    change_project_status,
    login_view,
    create_project
)


urlpatterns = [
    path(
        "management/",
        management_dashboard,
        name="management_dashboard"
    ),

    path(
        "management/team-leader/<int:user_id>/",
        management_team_leader,
        name="management_team_leader"
    ),

    path(
        "management/project/<int:project_id>/",
        management_project_detail,
        name="management_project_detail"
    ),
    path(
    "management/project/<int:project_id>/assign/",
    assign_project,
    name="assign_project"
    ),
    path(
    "management/project/<int:project_id>/status/",
    change_project_status,
    name="change_project_status"
    ),
    path(
        "login/",
        login_view,
        name="login"
    ),
    path(
    "management/project/create/",
    create_project,
    name="create_project"
    ),
]