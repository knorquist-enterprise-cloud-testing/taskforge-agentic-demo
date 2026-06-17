# Copilot instructions for TaskForge

TaskForge is a small Django app (templates frontend + JSON API backend + SQLite)
used to demo agentic development. Optimize for clarity over cleverness.

## Always
- Run `python manage.py test` and `python manage.py check` before you open or
  update a pull request. Report the result.
- Add or update tests in `tasks/tests.py` for any behavior you change.
- Keep changes surgical and scoped to the issue. Don't reformat unrelated files.
- Use only the Python standard library and Django unless the issue explicitly
  approves a new dependency (and then add it to `requirements.txt`).

## Architecture
- Frontend = server-rendered Django views in `tasks/views.py` + templates in
  `tasks/templates/tasks/`.
- Backend = JSON API in `tasks/api.py`, routed in `tasks/urls.py` under `/api/`.
- Serialization lives on the model: `Task.as_dict()`.

## Style
- 4-space indentation, descriptive names, short docstrings on public functions.
- Prefer `Task.STATUS_*` constants over string literals.

## Pull requests
- Title: imperative and specific.
- Body: what changed, why, and the exact test command output.
