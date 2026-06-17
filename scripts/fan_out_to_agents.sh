#!/usr/bin/env bash
#
# fan_out_to_agents.sh — Orchestrate MULTIPLE coding-agent sessions in parallel,
# programmatically, by assigning every `agent-ready` issue to GitHub Copilot
# cloud agent. Each assignment starts its own session and opens its own pull
# request, so you get N agents working at once — watch them in mission control
# (the Agents panel / github.com/copilot/agents).
#
# Requires: gh (authenticated), and Copilot cloud agent enabled on the repo.
# Docs: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api
#
# Usage:
#   ./scripts/fan_out_to_agents.sh                 # uses current repo, label "agent-ready"
#   REPO=owner/name LABEL=agent-ready ./scripts/fan_out_to_agents.sh
#   DRY_RUN=1 ./scripts/fan_out_to_agents.sh       # show what would happen
#
set -euo pipefail

REPO="${REPO:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
LABEL="${LABEL:-agent-ready}"
DRY_RUN="${DRY_RUN:-0}"
AGENT="copilot-swe-agent[bot]"

echo "Repo:  $REPO"
echo "Label: $LABEL"
echo

# 1. Confirm the coding agent can be assigned in this repo.
if ! gh api graphql -f query='
  query($owner:String!, $name:String!) {
    repository(owner:$owner, name:$name) {
      suggestedActors(capabilities:[CAN_BE_ASSIGNED], first:100) {
        nodes { login }
      }
    }
  }' -F owner="${REPO%/*}" -F name="${REPO#*/}" \
  --jq '.data.repository.suggestedActors.nodes[].login' 2>/dev/null \
  | grep -qx "copilot-swe-agent"; then
  echo "ERROR: Copilot cloud agent is not assignable in $REPO."
  echo "Enable it for the org/repo, then re-run. (suggestedActors did not include copilot-swe-agent.)"
  exit 1
fi

# 2. Find the open issues labelled for the agents.
mapfile -t ISSUES < <(gh issue list --repo "$REPO" --label "$LABEL" --state open --json number --jq '.[].number')

if [ "${#ISSUES[@]}" -eq 0 ]; then
  echo "No open issues with label '$LABEL'. Nothing to fan out."
  exit 0
fi

echo "Found ${#ISSUES[@]} issue(s) to delegate: ${ISSUES[*]}"
echo

# 3. Assign each one to Copilot — each becomes its own parallel agent session.
for n in "${ISSUES[@]}"; do
  title=$(gh issue view "$n" --repo "$REPO" --json title --jq .title)
  if [ "$DRY_RUN" = "1" ]; then
    echo "[dry-run] would assign #$n ($title) to $AGENT"
    continue
  fi
  echo "Assigning #$n ($title) -> $AGENT"
  gh api \
    --method POST \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "/repos/$REPO/issues/$n/assignees" \
    --input - >/dev/null <<JSON
{
  "assignees": ["copilot-swe-agent[bot]"],
  "agent_assignment": {
    "target_repo": "$REPO",
    "base_branch": "main",
    "custom_instructions": "Follow AGENTS.md. Add tests and run 'python manage.py test' before finishing."
  }
}
JSON
  echo "  -> session started; a draft PR will appear shortly."
done

echo
echo "Done. Track all sessions in mission control: https://github.com/copilot/agents"
