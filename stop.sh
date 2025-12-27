#!/usr/bin/env bash
set -e

PORT=5000
PID=$(lsof -ti tcp:${PORT} || true)

if [ -z "$PID" ]; then
  echo "Aucun serveur trouvé sur le port ${PORT}."
  exit 0
fi

echo "Arrêt du process (PID=${PID}) sur le port ${PORT}..."
kill "$PID"
echo "OK."
