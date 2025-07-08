#!/bin/bash
#run_django.sh - Local Django setup for SBA24070 Book Catalogue App
# Sets DB host to 'localhost' in settings.py
# Installs requirements, runs migrations, collects static, creates admin, and starts the Django server

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
check_and_install python3 python3
check_and_install pip python3-pip
check_and_install sed sed

# Check settings.py exists
if [ ! -f sba24070_book_catalogue/settings.py ]; then
  echo "[ERROR] sba24070_book_catalogue/settings.py not found."
  FAILED_STEPS+=("settings.py missing")
fi

# Set DB host to localhost using custom_scripts/host_helper.py if available
if [ -f custom_scripts/host_helper.py ]; then
  echo "[INFO] Setting DB host to 'localhost' using custom_scripts/host_helper.py..."
  python3 custom_scripts/host_helper.py <<< "1" || FAILED_STEPS+=("host_helper.py")
else
  echo "[WARN] custom_scripts/host_helper.py not found. Falling back to sed."
  sed -i "/'HOST':/c\        'HOST': 'localhost'," sba24070_book_catalogue/settings.py || FAILED_STEPS+=("sed db host")
fi

# Activate virtual environment (assume 'devops' by default)
if [ -d "devops" ]; then
  source devops/bin/activate
else
  echo "Virtual environment 'devops' not found. Creating..."
  python3 -m venv devops || FAILED_STEPS+=("venv creation")
  source devops/bin/activate
fi

# Install requirements
pip install --upgrade pip || FAILED_STEPS+=("pip upgrade")
pip install -r requirements.txt || FAILED_STEPS+=("pip requirements")

# Run migrations and collect static files
python manage.py makemigrations || FAILED_STEPS+=("makemigrations")
python manage.py migrate || FAILED_STEPS+=("migrate")
python manage.py collectstatic --noinput || FAILED_STEPS+=("collectstatic")

# Create admin user
python custom_scripts/admin_manager.py || FAILED_STEPS+=("admin_manager.py")

echo "\n[INFO] App ready! Visit: http://127.0.0.1:8000"
echo "[INFO] Admin login: admin / admin"

echo "[INFO] Starting Django development server..."
# Start Django server
python manage.py runserver || FAILED_STEPS+=("runserver")

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