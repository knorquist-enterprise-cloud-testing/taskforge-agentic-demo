# TaskForge — a demo app for GitHub agentic development

TaskForge is a deliberately small **Django** task tracker built to demonstrate
GitHub's **agentic development** capabilities — especially **orchestrating
multiple agent sessions**, including **programmatically** (Copilot CLI
non-interactively and via GitHub Actions).

- **Frontend:** Django server-rendered templates (`tasks/views.py`, `tasks/templates/`)
- **Backend:** a small JSON API (`tasks/api.py`) at `/api/tasks/`
- **Database:** SQLite (zero-config)

> Built for the Okta × GitHub *Agentic Development* enablement session.
> See **[DEMOS.md](DEMOS.md)** for the run-of-show, and the repo's **Issues** tab
> for ready-to-run agent tasks.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # optional: a few sample tasks
python manage.py runserver     # http://127.0.0.1:8000
```

Run the tests:

```bash
python manage.py test
```

## What it demonstrates

| Capability | Where to look |
|---|---|
| **Copilot coding agent** — assign an issue, get a PR | Issues labelled `demo:coding-agent` |
| **Programmatic fan-out** — N parallel agent sessions from a script | `scripts/fan_out_to_agents.sh` + issues labelled `agent-ready` |
| **Copilot CLI, non-interactive** — `copilot -p ...` in scripts | `scripts/cli_examples.sh` |
| **Copilot CLI in GitHub Actions** — agent in CI | `.github/workflows/agentic-triage.yml` |
| **Custom agents / sub-agents** — scoped specialists | `.github/agents/` |
| **Agent context files** — steer every agent | `AGENTS.md`, `.github/copilot-instructions.md` |

## Project layout

```
taskforge/            Django project (settings, urls, wsgi/asgi)
tasks/                the app: models, views (frontend), api.py (backend), tests
  templates/tasks/    HTML templates
  management/commands/seed.py
.github/
  agents/             custom agent profiles (test-writer, api-designer, bug-fixer)
  workflows/          ci.yml + agentic-triage.yml (Copilot CLI in Actions)
  copilot-instructions.md
scripts/              fan_out_to_agents.sh, cli_examples.sh
AGENTS.md             project context for any AGENTS.md-aware agent
DEMOS.md              facilitator run-of-show
```

## Note
This app is intentionally minimal and **not production-hardened** (demo secret
key, `csrf_exempt` API, `ALLOWED_HOSTS = ["*"]`). Don't ship it as-is.
