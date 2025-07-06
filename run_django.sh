#!/bin/bash
set -e

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

echo "\nApp ready! Visit: http://127.0.0.1:8000"
echo "Admin login: admin / admin"

# Start Django server
python manage.py runserver 