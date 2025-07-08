#!/bin/bash
#run_django.sh - Local Django setup for SBA24070 Book Catalogue App
# Sets DB host to 'localhost' in settings.py
# Installs requirements, runs migrations, collects static, creates admin, and starts the Django server

set -e

# Tool checks
command -v python3 >/dev/null 2>&1 || { echo >&2 "[ERROR] Python 3 is not installed. Aborting."; exit 1; }
command -v pip >/dev/null 2>&1 || { echo >&2 "[ERROR] pip is not installed. Aborting."; exit 1; }
command -v sed >/dev/null 2>&1 || { echo >&2 "[ERROR] sed is not installed. Aborting."; exit 1; }

# Check settings.py exists
if [ ! -f sba24070_book_catalogue/settings.py ]; then
  echo "[ERROR] sba24070_book_catalogue/settings.py not found. Aborting."
  exit 1
fi

# Set DB host to localhost
sed -i "/'HOST':/c\        'HOST': 'localhost'," sba24070_book_catalogue/settings.py

# Activate virtual environment (assume 'devops' by default)
if [ -d "devops" ]; then
  source devops/bin/activate
else
  echo "Virtual environment 'devops' not found. Creating..."
  python3 -m venv devops
  source devops/bin/activate
fi

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations and collect static files
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Create admin user
python admin_manager.py

echo "\n[INFO] App ready! Visit: http://127.0.0.1:8000"
echo "[INFO] Admin login: admin / admin"

echo "[INFO] Starting Django development server..."
# Start Django server
python manage.py runserver 