"""Tests for the TaskForge tasks app."""
import json

from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTests(TestCase):
    def test_str_returns_title(self):
        task = Task.objects.create(title="Write docs")
        self.assertEqual(str(task), "Write docs")

    def test_new_task_defaults_to_todo(self):
        task = Task.objects.create(title="Default status")
        self.assertEqual(task.status, Task.STATUS_TODO)
        self.assertFalse(task.is_done)

    def test_as_dict_includes_core_fields(self):
        task = Task.objects.create(title="Serialize me", description="hi")
        data = task.as_dict()
        self.assertEqual(data["title"], "Serialize me")
        self.assertEqual(data["description"], "hi")
        self.assertEqual(data["status"], Task.STATUS_TODO)
        self.assertFalse(data["is_done"])


class FrontendViewTests(TestCase):
    def test_index_renders(self):
        Task.objects.create(title="Visible task")
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visible task")

    def test_add_task_creates_record(self):
        response = self.client.post(
            reverse("tasks:add_task"), {"title": "From form", "description": ""}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="From form").exists())

    def test_add_task_requires_title(self):
        response = self.client.post(reverse("tasks:add_task"), {"title": "  "})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_toggle_marks_done_then_todo(self):
        task = Task.objects.create(title="Toggle me")
        self.client.post(reverse("tasks:toggle_task", args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.is_done)
        self.client.post(reverse("tasks:toggle_task", args=[task.id]))
        task.refresh_from_db()
        self.assertFalse(task.is_done)

    def test_delete_removes_record(self):
        task = Task.objects.create(title="Delete me")
        self.client.post(reverse("tasks:delete_task", args=[task.id]))
        self.assertFalse(Task.objects.filter(pk=task.id).exists())


class ApiTests(TestCase):
    def test_list_returns_json(self):
        Task.objects.create(title="API task")
        response = self.client.get(reverse("tasks:api_task_list"))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["count"], 1)
        self.assertEqual(body["tasks"][0]["title"], "API task")

    def test_create_via_post(self):
        response = self.client.post(
            reverse("tasks:api_task_list"),
            data=json.dumps({"title": "Created via API"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Task.objects.filter(title="Created via API").exists())

    def test_create_requires_title(self):
        response = self.client.post(
            reverse("tasks:api_task_list"),
            data=json.dumps({"description": "no title"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
