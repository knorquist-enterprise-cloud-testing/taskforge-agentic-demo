"""JSON API for TaskForge (the Python backend).

This is a deliberately small, dependency-free JSON API built on Django views.
It exists so that agentic-development demos have a backend surface to extend
(for example, adding a statistics endpoint).
"""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Task


def task_list(request):
    """GET  /api/tasks/  -> list tasks.
    POST /api/tasks/  -> create a task from a JSON body.
    """
    if request.method == "GET":
        tasks = [task.as_dict() for task in Task.objects.all()]
        return JsonResponse({"tasks": tasks, "count": len(tasks)})

    if request.method == "POST":
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body."}, status=400)

        title = (payload.get("title") or "").strip()
        if not title:
            return JsonResponse({"error": "Field 'title' is required."}, status=400)

        task = Task.objects.create(
            title=title,
            description=(payload.get("description") or "").strip(),
            status=payload.get("status") or Task.STATUS_TODO,
        )
        return JsonResponse(task.as_dict(), status=201)

    return JsonResponse({"error": "Method not allowed."}, status=405)


# csrf_exempt keeps the demo API easy to call with curl. Do not copy this into
# a production service without real authentication.
task_list = csrf_exempt(task_list)
