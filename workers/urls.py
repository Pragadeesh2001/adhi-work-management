from django.urls import path
from .views import add_worker, edit_worker,  delete_worker


urlpatterns = [
    path(
        "project/<int:project_id>/add-worker/",
        add_worker,
        name="add_worker"
    ),
     path(
        "worker/<int:worker_id>/edit/",
        edit_worker,
        name="edit_worker",
    ),
    path(
    "worker/<int:worker_id>/delete/",
    delete_worker,
    name="delete_worker",
),
]