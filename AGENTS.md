# Project context for AI agents

> This file is read by GitHub Copilot agents (coding agent, CLI, IDE) and other
> `AGENTS.md`-aware tools. Keep it short, specific, and current.

## What this is
TaskForge is a deliberately small Django task-tracker used to demonstrate
GitHub's agentic development capabilities. Frontend = Django templates,
backend = a small JSON API (`tasks/api.py`), database = SQLite.

## Project layout
- `taskforge/` — Django project (settings, urls, wsgi/asgi)
- `tasks/` — the single app
  - `models.py` — `Task` model
  - `views.py` — server-rendered frontend
  - `api.py` — JSON API (the "backend")
  - `tests.py` — Django `TestCase` suite
  - `templates/tasks/` — HTML templates
- `.github/agents/` — custom agent profiles
- `.github/workflows/` — CI + an agentic-orchestration workflow
- `scripts/` — helper scripts for the demos

## How to set up and run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # optional sample data
python manage.py runserver
```

## How to validate your work (always do this before finishing)
```bash
python manage.py test          # run the full suite
python manage.py check         # Django system checks
```
All tests must pass. If you add a feature, add tests for it. If you fix a bug,
add a regression test that fails before your fix and passes after.

## Conventions
- Python, 4-space indentation, standard library + Django only (no new runtime deps
  without calling it out in the PR description).
- Keep views thin; put serialization on the model (`Task.as_dict`).
- Match the existing style; do not reformat unrelated code.
- Never commit `db.sqlite3` or `.venv/`.

## Good first tasks for agents
See the open issues and `DEMOS.md`.
