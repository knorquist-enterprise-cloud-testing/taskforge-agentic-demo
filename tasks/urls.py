"""URL routing for the tasks app (frontend + JSON API)."""
from django.urls import path

from . import api, views

app_name = "tasks"

urlpatterns = [
    # Frontend (server-rendered)
    path("", views.index, name="index"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/<int:task_id>/toggle/", views.toggle_task, name="toggle_task"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    # Backend JSON API
    path("api/tasks/", api.task_list, name="api_task_list"),
]
