#!/bin/bash
set -e # stop on error
# Run from the base directory, not from repository
url="postgresql://postgres:password@localhost:5432/postgres?sslmode=disable"
echo -n "waiting for backend database to be ready ..."
iteration=0
timeout=30
ready=0
until [[ $ready -eq 1 ]]; do
  if psql $url -c 'SELECT 1;' &> /dev/null; then
    ready=1
  else
    iteration=$(( iteration + 1 ))
    if [[ $iteration -gt $timeout ]]; then
      echo " timed out after $timeout seconds"
      exit 1
    fi
    sleep 1
    echo -n "."
  fi
done
echo " ok"
atlas schema apply --auto-approve \
  --url $url \
  --to file://repository/schema/schema.sql \
  --dev-url "postgresql://postgres:password@localhost:5432/postgres?sslmode=disable" > /dev/null

# psql -v ON_ERROR_STOP=1 --file="testdata/generated.sql" $url > /dev/null
psql -v ON_ERROR_STOP=1 --file="repository/testdata/testdata.sql" $url > /dev/null