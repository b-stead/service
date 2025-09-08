#!/bin/bash
set -e # stop on error
opts="--project-directory=. --project-name=service_app --file=repository/compose.yaml --file=backend/compose.yaml"
docker compose $opts up --detach
trap "docker compose $opts down" EXIT
source repository/apply.sh

docker compose $opts up