"""Seed the database with a few sample tasks for demos."""
from django.core.management.base import BaseCommand

from tasks.models import Task

SAMPLE_TASKS = [
    ("Welcome to TaskForge", "Edit or delete me — I'm just sample data.", Task.STATUS_DONE),
    ("Try the Copilot coding agent", "Assign an issue to Copilot and watch it open a PR.", Task.STATUS_TODO),
    ("Run Copilot CLI non-interactively", "copilot -p '...' --allow-tool=...", Task.STATUS_DOING),
    ("Orchestrate agents in Actions", "See .github/workflows/agentic-triage.yml", Task.STATUS_TODO),
]


class Command(BaseCommand):
    help = "Populate the database with sample tasks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete existing tasks before seeding.",
        )

    def handle(self, *args, **options):
        if options["fresh"]:
            deleted, _ = Task.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing rows."))

        created = 0
        for title, description, status in SAMPLE_TASKS:
            _, was_created = Task.objects.get_or_create(
                title=title,
                defaults={"description": description, "status": status},
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} task(s)."))
