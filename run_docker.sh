#!/bin/bash

#run_docker.sh - Docker setup for SBA24070 Book Catalogue App
#Sets DB host to 'db' in settings.py
#Builds and starts Docker containers, runs migrations, collects static, creates admin

set -e

# Set DB host to db
sed -i "/'HOST':/c\        'HOST': 'db'," sba24070_book_catalogue/settings.py

echo "Building and starting Docker containers..."
docker compose up --build -d

echo "Running migrations, collectstatic, and admin creation in the web container..."
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py create_admin

echo "\n[INFO] App ready! Visit: http://localhost:8000"
echo "[INFO] Admin login: admin / admin"
echo "[INFO] To stop: docker compose down" 