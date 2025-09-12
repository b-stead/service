#!/bin/bash
if [[ -f .venv/bin/activate ]]; then source .venv/bin/activate; fi
flake8 backend