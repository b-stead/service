#!/bin/bash
set -e # stop on error
if [[ -f .venv/bin/activate ]]; then source .venv/bin/activate; fi

echo "generate python client from database schema and queries: sqlc generate"
sqlc generate --file=repository/sqlc.yaml
repository/fix.py backend/repository/*.py
# repository/fix.py worker/repository/*.py

echo "generate OpenAPI spec from FastAPI app: python -m backend.gen"
export SECRET_KEY=foo
export DOCS_PASSWORD=bar
export TOKEN_ISSUER=beep
export TOKEN_AUDIENCE=boop
python -m backend.gen