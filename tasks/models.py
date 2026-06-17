"""Data models for TaskForge."""
from django.db import models


class Task(models.Model):
    """A single unit of work tracked in TaskForge."""

    STATUS_TODO = "todo"
    STATUS_DOING = "doing"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_TODO, "To do"),
        (STATUS_DOING, "In progress"),
        (STATUS_DONE, "Done"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_done(self):
        return self.status == self.STATUS_DONE

    def as_dict(self):
        """Serialize the task for the JSON API."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "is_done": self.is_done,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
