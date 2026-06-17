#!/usr/bin/env bash
#
# cli_examples.sh — A tour of GitHub Copilot CLI in NON-INTERACTIVE (programmatic)
# mode. Every command uses `-p` so Copilot runs once and exits, making it usable
# in scripts, pipes, and CI. Tools are allow-listed explicitly (least privilege).
#
# Prereqs:
#   npm install -g @github/copilot      # install the CLI
#   copilot                             # run once, then /login to authenticate
#
# Run a single example:   ./scripts/cli_examples.sh 3
# List the examples:      ./scripts/cli_examples.sh
#
set -euo pipefail

run() { echo "+ $*"; eval "$*"; }

case "${1:-}" in
  1)
    # Explain a file (read-only, silent output).
    run "copilot -p 'Summarize what tasks/api.py does in under 80 words' -s"
    ;;
  2)
    # Generate a commit message for staged changes.
    run "copilot -p 'Write a one-line, imperative commit message for the staged changes' -s --allow-tool='shell(git:*)'"
    ;;
  3)
    # Add tests, letting Copilot run the suite to verify (least-privilege tools).
    run "copilot -p 'Add a test to tasks/tests.py for the /api/tasks/ POST error path, then run python manage.py test' \
          --allow-tool=write --allow-tool='shell(python:*)' --no-ask-user"
    ;;
  4)
    # Use the built-in code-review agent on the current branch vs main.
    run "copilot -p '/review the changes on this branch compared to main. Focus on bugs and security.' -s --allow-tool='shell(git:*)'"
    ;;
  5)
    # Capture Copilot output into a shell variable (scripting pattern).
    run "ver=\$(copilot -p 'What Django version does requirements.txt require? Answer with the spec only.' -s); echo \"Django spec: \$ver\""
    ;;
  6)
    # Hands-off: autopilot mode, full permissions, capped continuations.
    # Best run in a sandbox or CI. Implements an issue end-to-end.
    run "copilot --autopilot --yolo --max-autopilot-continues 12 \
          -p 'Implement a GET /api/stats/ endpoint returning counts by status, with tests. Run python manage.py test.'"
    ;;
  *)
    cat <<'EOF'
GitHub Copilot CLI — programmatic examples. Pass a number to run one:

  1  Explain a file (read-only)
  2  Generate a commit message from staged changes
  3  Add a test and run the suite (least-privilege tools)
  4  Code-review this branch with the built-in code-review agent
  5  Capture Copilot output into a shell variable
  6  Autopilot: implement an endpoint end-to-end, hands-off (use in a sandbox/CI)

Example:  ./scripts/cli_examples.sh 1
EOF
    ;;
esac
