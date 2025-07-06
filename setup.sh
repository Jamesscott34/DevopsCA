#!/bin/bash
'''
setup.sh - Interactive setup for SBA24070 Book Catalogue App
- Asks if you want to run locally (Django) or with Docker
- Sets the correct DB host in settings.py
- Installs requirements, runs migrations, collects static, creates admin, and starts the app in the chosen mode
'''
set -e

# Function to update DB host in settings.py
update_db_host() {
    local host_value="$1"
    sed -i "/'HOST':/c\        'HOST': '$host_value'," sba24070_book_catalogue/settings.py
    echo "[INFO] Set DB host to '$host_value' in settings.py"
}

echo "=========================================="
echo " SBA24070 Book Catalogue Setup Script"
echo "=========================================="
echo "Choose setup mode:"
echo "1) Local Django (no Docker)"
echo "2) Docker Compose"
read -p "Enter 1 or 2: " mode

if [ "$mode" = "1" ]; then
    '''
    Local Django setup
    '''
    update_db_host "localhost"
    if [ ! -d "devops" ]; then
        echo "[INFO] Creating virtual environment 'devops'..."
        python3 -m venv devops
    fi
    source devops/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --noinput
    python admin_manager.py
    echo "\n[INFO] App ready! Visit: http://127.0.0.1:8000"
    echo "[INFO] Admin login: admin / admin"
    python manage.py runserver
elif [ "$mode" = "2" ]; then
    '''
    Docker Compose setup
    '''
    update_db_host "db"
    docker compose up --build -d
    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py collectstatic --noinput
    docker compose exec web python manage.py create_admin
    echo "\n[INFO] App ready! Visit: http://localhost:8000"
    echo "[INFO] Admin login: admin / admin"
    echo "[INFO] To stop: docker compose down"
else
    echo "[ERROR] Invalid selection. Exiting."
    exit 1
fi 