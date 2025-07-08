#!/bin/bash

#run_docker.sh - Docker setup for SBA24070 Book Catalogue App
#Sets DB host to 'db' in settings.py
#Builds and starts Docker containers, runs migrations, collects static, creates admin

# Remove 'set -e' for custom error handling
FAILED_STEPS=()

# Tool check and install helper
check_and_install() {
  local tool="$1"
  local pkg="$2"
  if ! command -v "$tool" >/dev/null 2>&1; then
    read -p "[PROMPT] $tool is not installed. Install it now with sudo apt install $pkg? [y/n]: " install_tool
    if [[ "$install_tool" =~ ^[Yy]$ ]]; then
      sudo apt-get update && sudo apt-get install -y "$pkg"
      if ! command -v "$tool" >/dev/null 2>&1; then
        echo "[ERROR] $tool installation failed."
        FAILED_STEPS+=("$tool install failed")
      fi
    else
      echo "[ERROR] $tool is required. Skipping $tool-dependent steps."
      FAILED_STEPS+=("$tool declined")
    fi
  fi
}

# Tool checks (with install prompt)
check_and_install docker docker.io
check_and_install sed sed
# Check for docker compose (plugin or legacy)
if ! docker compose version >/dev/null 2>&1 && ! command -v docker-compose >/dev/null 2>&1; then
  read -p "[PROMPT] Docker Compose is not installed. Install it now with sudo apt install docker-compose? [y/n]: " install_compose
  if [[ "$install_compose" =~ ^[Yy]$ ]]; then
    sudo apt-get update && sudo apt-get install -y docker-compose
    if ! docker compose version >/dev/null 2>&1 && ! command -v docker-compose >/dev/null 2>&1; then
      echo "[ERROR] Docker Compose installation failed."
      FAILED_STEPS+=("docker compose install failed")
    fi
  else
    echo "[ERROR] Docker Compose is required. Skipping docker-compose-dependent steps."
    FAILED_STEPS+=("docker compose declined")
  fi
fi

# Check settings.py exists
if [ ! -f sba24070_book_catalogue/settings.py ]; then
  echo "[ERROR] sba24070_book_catalogue/settings.py not found."
  FAILED_STEPS+=("settings.py missing")
fi

# Set DB host to db using custom_scripts/host_helper.py if available
if [ -f custom_scripts/host_helper.py ]; then
  echo "[INFO] Setting DB host to 'db' using custom_scripts/host_helper.py..."
  python3 custom_scripts/host_helper.py <<< "2" || FAILED_STEPS+=("host_helper.py")
else
  echo "[WARN] custom_scripts/host_helper.py not found. Falling back to sed."
  sed -i "/'HOST':/c\        'HOST': 'db'," sba24070_book_catalogue/settings.py || FAILED_STEPS+=("sed db host")
fi

echo "Building and starting Docker containers..."
docker compose up --build -d || docker-compose up --build -d || FAILED_STEPS+=("docker compose up")

echo "Running migrations, collectstatic, and admin creation in the web container..."
docker compose exec web python manage.py migrate || docker-compose exec web python manage.py migrate || FAILED_STEPS+=("migrate")
docker compose exec web python manage.py collectstatic --noinput || docker-compose exec web python manage.py collectstatic --noinput || FAILED_STEPS+=("collectstatic")
docker compose exec web python manage.py create_admin || docker-compose exec web python manage.py create_admin || FAILED_STEPS+=("create_admin")

echo "\n[INFO] App ready! Visit: http://localhost:8000"
echo "[INFO] Admin login: admin / admin"
echo "[INFO] To stop: docker compose down or docker-compose down"

# Print summary of failed steps if any
if [ ${#FAILED_STEPS[@]} -ne 0 ]; then
  echo "\n[SUMMARY] The following steps failed or were skipped:"
  for step in "${FAILED_STEPS[@]}"; do
    echo "  - $step"
  done
  echo "[INFO] Please review the errors above and resolve as needed."
else
  echo "\n[INFO] All steps completed (or skipped with user permission)."
fi 