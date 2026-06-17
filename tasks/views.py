"""Server-rendered views (the TaskForge frontend)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Task


def index(request):
    """Render the task board with a count of remaining (open) work."""
    tasks = Task.objects.all()

    # The "remaining" badge in the header should reflect how many tasks are
    # still open (not yet done). See the open issue describing the incorrect
    # count for the expected behavior.
    remaining = Task.objects.count()

    return render(
        request,
        "tasks/index.html",
        {"tasks": tasks, "remaining": remaining},
    )


def add_task(request):
    """Create a new task from the board form."""
    if request.method != "POST":
        return redirect("tasks:index")

    title = (request.POST.get("title") or "").strip()
    description = (request.POST.get("description") or "").strip()

    if not title:
        messages.error(request, "A task needs a title.")
        return redirect("tasks:index")

    Task.objects.create(title=title, description=description)
    messages.success(request, "Task added.")
    return redirect("tasks:index")


def toggle_task(request, task_id):
    """Toggle a task between done and to-do."""
    if request.method != "POST":
        return redirect("tasks:index")

    task = get_object_or_404(Task, pk=task_id)
    task.status = Task.STATUS_TODO if task.is_done else Task.STATUS_DONE
    task.save(update_fields=["status", "updated_at"])
    return redirect("tasks:index")


def delete_task(request, task_id):
    """Delete a task."""
    if request.method != "POST":
        return redirect("tasks:index")

    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect("tasks:index")
