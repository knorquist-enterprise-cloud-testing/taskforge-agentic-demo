"""JSON API for TaskForge (the Python backend).

This is a deliberately small, dependency-free JSON API built on Django views.
It exists so that agentic-development demos have a backend surface to extend
(for example, adding a statistics endpoint).
"""
import json

from django.db.models import Count
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


def api_stats(request):
    """GET /api/stats/ -> aggregate task statistics."""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed."}, status=405)

    rows = Task.objects.values("status").annotate(count=Count("id"))
    by_status = {Task.STATUS_TODO: 0, Task.STATUS_DOING: 0, Task.STATUS_DONE: 0}
    for row in rows:
        by_status[row["status"]] = row["count"]

    total = sum(by_status.values())
    open_count = by_status[Task.STATUS_TODO] + by_status[Task.STATUS_DOING]
    return JsonResponse({"total": total, "by_status": by_status, "open": open_count})


# csrf_exempt keeps the demo API easy to call with curl. Do not copy this into
# a production service without real authentication.
task_list = csrf_exempt(task_list)
