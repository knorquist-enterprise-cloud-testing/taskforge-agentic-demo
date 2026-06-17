# TaskForge — facilitator run-of-show

Five demos, ~45 minutes, escalating from one agent to many — and from clicks to
code. Each maps to an open issue in this repo. Do them in order; later demos
reuse the muscle memory of earlier ones.

> **Before the session:** `python manage.py migrate && python manage.py seed`,
> confirm Copilot cloud agent is enabled for the org/repo, and add the
> `COPILOT_CLI_TOKEN` secret (fine-grained PAT with **Copilot Requests**) if you
> want to run Demo 4 live.

---

## Demo 1 — One agent, issue → pull request (the "hello world")
**Issue:** *Add due dates to tasks* — label `demo:coding-agent`
**Surface:** Copilot cloud agent (coding agent), in the browser.

1. Open the issue. In the sidebar, set **Assignees → Copilot**.
2. Copilot adds 👀, starts a session, and opens a **draft PR** linked to the issue.
3. Open the PR → **View session** to watch its reasoning live.
4. When done, add **Copilot** as a **Reviewer** to show AI code review on the PR.

**Talking point:** the agent runs in an ephemeral GitHub Actions environment,
reads `AGENTS.md` / `copilot-instructions.md`, and validates with the test suite.

---

## Demo 2 — Many agents in parallel, PROGRAMMATICALLY (the headline)
**Issues:** the three labelled `agent-ready`
( *Add CSV export*, *Add full-text task search*, *Add a `/api/stats/` endpoint* )
**Surface:** REST API + a shell script → mission control.

```bash
# Dry run first to show what it will do:
DRY_RUN=1 ./scripts/fan_out_to_agents.sh

# Then fan out for real — one agent session per issue, in parallel:
./scripts/fan_out_to_agents.sh
```

1. The script verifies the agent is assignable (`suggestedActors`), finds every
   open `agent-ready` issue, and assigns each to `copilot-swe-agent[bot]`.
2. Open **mission control** (`https://github.com/copilot/agents`) to watch all
   three sessions run **at the same time**, each opening its own PR.

**Talking point:** this is the core of "orchestrating multiple agents
programmatically." The same thing is possible from CI, a cron job, or your own
tool via the REST/GraphQL **agent tasks API**.

---

## Demo 3 — Copilot CLI, non-interactive, fixes a real bug
**Issue:** *Remaining counter includes completed tasks* — label `demo:cli`
**Surface:** Copilot CLI in the terminal (programmatic `-p`).

There is a **genuine seeded bug**: the header badge shows the count of *all*
tasks instead of only the open ones (see `tasks/views.py`, `index()`). With 4
seeded tasks (1 done) the badge reads **"4 remaining"** but should read **"3"**.

```bash
copilot -p "In tasks/views.py the 'remaining' badge counts all tasks instead of
  only open ones. Fix it, add a regression test in tasks/tests.py, and run
  python manage.py test." \
  --allow-tool=write --allow-tool='shell(python:*)' --no-ask-user
```

Then show the other one-liners: `./scripts/cli_examples.sh` (explain, commit
message, review, autopilot). 

**Talking point:** the exact same prompt works interactively, in this script, or
in CI — that's the point of programmatic mode.

---

## Demo 4 — An agent inside GitHub Actions
**Surface:** `.github/workflows/agentic-triage.yml`

1. **Actions** tab → **Agentic triage (Copilot CLI)** → **Run workflow**.
2. It installs Copilot CLI on the runner and runs `copilot -p` non-interactively
   to write a weekly project digest into the run summary.

**Talking point:** Copilot CLI is "just a CLI" on the runner — schedule it,
trigger it on events, or chain it into existing pipelines. Authentated with a
scoped PAT stored as a secret.

---

## Demo 5 — Custom agents & sub-agent orchestration
**Surface:** `.github/agents/` + Copilot CLI / cloud agent.

- Show the three scoped specialists: `test-writer`, `api-designer`, `bug-fixer`.
- In the CLI: `copilot --agent=test-writer -p "raise coverage on tasks/api.py"`.
- Or assign an issue to a custom agent from the issue's agent dropdown.

**Talking point:** scoped tools + scoped prompts = safer, more predictable
agents. A parent session can delegate to these as **sub-agents** automatically.

---

## One-line recap for the room
> Start with one agent on one issue → fan out to many agents from a script →
> drop the same agent into the terminal and into CI. Same engine, three levels
> of orchestration, all governed by your repo's context files and permissions.
