#!/bin/bash

#run_docker.sh - Docker setup for SBA24070 Book Catalogue App
#Sets DB host to 'db' in settings.py
#Builds and starts Docker containers, runs migrations, collects static, creates admin

set -e

# Tool checks
command -v docker >/dev/null 2>&1 || { echo >&2 "[ERROR] Docker is not installed. Aborting."; exit 1; }
command -v sed >/dev/null 2>&1 || { echo >&2 "[ERROR] sed is not installed. Aborting."; exit 1; }
# Check for docker compose (plugin or legacy)
if ! docker compose version >/dev/null 2>&1 && ! command -v docker-compose >/dev/null 2>&1; then
  echo >&2 "[ERROR] Docker Compose is not installed or not available as a plugin. Aborting."
  exit 1
fi

# Check settings.py exists
if [ ! -f sba24070_book_catalogue/settings.py ]; then
  echo "[ERROR] sba24070_book_catalogue/settings.py not found. Aborting."
  exit 1
fi

# Set DB host to db
sed -i "/'HOST':/c\        'HOST': 'db'," sba24070_book_catalogue/settings.py

echo "Building and starting Docker containers..."
docker compose up --build -d || docker-compose up --build -d

echo "Running migrations, collectstatic, and admin creation in the web container..."
docker compose exec web python manage.py migrate || docker-compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput || docker-compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py create_admin || docker-compose exec web python manage.py create_admin

echo "\n[INFO] App ready! Visit: http://localhost:8000"
echo "[INFO] Admin login: admin / admin"
echo "[INFO] To stop: docker compose down or docker-compose down" 