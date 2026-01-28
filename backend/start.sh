#!/usr/bin/env bash
set -euo pipefail

DB_DISK_PATH="/app/data/lux_data_2026_map.db"
DB_BUNDLED_PATH="$(pwd)/backend/lux_data_2026_map.db"

mkdir -p /app/data

# If disk DB doesn't exist yet, seed it from the bundled DB
if [ ! -f "$DB_DISK_PATH" ]; then
  echo "No DB on disk. Seeding from bundled DB..."
  if [ ! -f "$DB_BUNDLED_PATH" ]; then
    echo "ERROR: Bundled DB not found at $DB_BUNDLED_PATH"
    ls -la "$(pwd)/backend" || true
    exit 1
  fi
  cp "$DB_BUNDLED_PATH" "$DB_DISK_PATH"
fi

echo "DB file info:"
ls -la "$DB_DISK_PATH" || true

cd backend
exec uvicorn main_api:app --host 0.0.0.0 --port "${PORT}"