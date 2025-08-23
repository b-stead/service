#!/bin/bash
set -e # stop on error
opts="--project-directory=. --project-name=service_app --file=repository/compose.yaml"
docker compose $opts up --detach
trap "docker compose $opts down" EXIT
source repository/apply.sh
echo "apply completed"
source ../.venv/bin/activate
echo "Starting backend server..."
export SECRET_KEY=foo
export DOCS_PASSWORD=bar
export LOG_STYLE=console
export TOKEN_AUDIENCE=beep
export TOKEN_ISSUER=boop
uvicorn backend.main:app --reload --log-config=backend/uvicorn_log_config.yaml
