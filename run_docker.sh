#!/bin/bash
set -e

echo "Building and starting Docker containers..."
docker compose up --build -d

echo "Running migrations, collectstatic, and admin creation in the web container..."
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py create_admin

echo "\nApp ready! Visit: http://localhost:8000"
echo "Admin login: admin / admin"
echo "To stop: docker compose down" 