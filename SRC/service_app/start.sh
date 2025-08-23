#!/bin/bash
set -e # stop on error
opts="--project-directory=. --project-name=service_app --file=repository/compose.yaml --file=backend/compose.yaml"
docker compose $opts up --detach
# trap "docker compose $opts down" EXIT

# Check the status of the containers
echo "Checking container statuses..."
docker compose $opts ps

# Debugging: Show logs for all services
echo "Fetching logs for all services..."
docker compose $opts logs --no-color > service_app_logs.txt
echo "Logs saved to service_app_logs.txt"


source repository/apply.sh
# url="postgresql://postgres:password@localhost:5433/service_app?sslmode=disable"
# echo -n "waiting for frontend database to be ready ..."
# iteration=0
# timeout=30
# ready=0
# until [[ $ready -eq 1 ]]; do
#     if psql $url -c 'SELECT 1;' &> /dev/null; then
#         ready=1
#     else
#         iteration=$(( iteration + 1 ))
#     if [[ $iteration -gt $timeout ]]; then
#         echo " timed out after $timeout seconds"
#         exit 1
#     fi
#     sleep 1
#     echo -n "."
#     fi
# done
echo "apply completed"
echo " ok"
