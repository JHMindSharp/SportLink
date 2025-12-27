#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Active le venv
source .venv/bin/activate

# Variables Flask
export FLASK_APP="app:create_app"
export FLASK_ENV=development
export FLASK_DEBUG=1

# Lance Flask en arrière-plan
flask run --host=127.0.0.1 --port=5000 &
PID=$!

# Ouvre le navigateur
sleep 1
open "http://127.0.0.1:5000"

# Garde le script vivant tant que Flask tourne
wait $PID
