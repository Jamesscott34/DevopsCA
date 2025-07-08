#!/bin/bash
# run_kuber.sh - Kubernetes deployment automation for SBA24070 Book Catalogue App
# Builds image (if needed), applies manifests, waits for pod, runs migrations, opens service

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
check_and_install docker docker.io
check_and_install curl curl
check_and_install kubectl kubectl
check_and_install minikube minikube

# If nuitka is installed, create venv and install requirements
if command -v nuitka >/dev/null 2>&1; then
  echo "[INFO] nuitka detected. Ensuring Python virtual environment and requirements."
  if [ ! -d "devops" ]; then
    echo "[INFO] Creating Python virtual environment 'devops'..."
    python3 -m venv devops || FAILED_STEPS+=("venv creation")
  fi
  source devops/bin/activate
  pip install --upgrade pip || FAILED_STEPS+=("pip upgrade")
  pip install -r requirements.txt || FAILED_STEPS+=("pip requirements")
fi

# Set DB host to db using host_helper.py if available
if [ -f host_helper.py ]; then
  echo "[INFO] Setting DB host to 'db' using host_helper.py..."
  python3 host_helper.py <<< "2" || FAILED_STEPS+=("host_helper.py")
else
  echo "[WARN] host_helper.py not found. Falling back to sed."
  sed -i "/'HOST':/c\        'HOST': 'db'," sba24070_book_catalogue/settings.py || FAILED_STEPS+=("sed db host")
fi

# Optionally build and push Docker image (uncomment if needed)
# echo "[INFO] Building Docker image..."
# docker build -t your-dockerhub-username/devops-book-app:latest .
# echo "[INFO] Pushing Docker image to registry..."
# docker push your-dockerhub-username/devops-book-app:latest

# Apply Kubernetes manifests
kubectl apply -f k8s/secret.yaml || FAILED_STEPS+=("kubectl secret.yaml")
kubectl apply -f k8s/configmap.yaml || FAILED_STEPS+=("kubectl configmap.yaml")
kubectl apply -f k8s/postgres-deployment.yaml || FAILED_STEPS+=("kubectl postgres-deployment.yaml")
kubectl apply -f k8s/deployment.yaml || FAILED_STEPS+=("kubectl deployment.yaml")
kubectl apply -f k8s/service.yaml || FAILED_STEPS+=("kubectl service.yaml")

echo "[INFO] Waiting for Django pod to be running..."
WAIT_COUNT=0
while true; do
  DJANGO_POD=$(kubectl get pods -l app=django -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
  STATUS=$(kubectl get pod "$DJANGO_POD" -o jsonpath='{.status.phase}' 2>/dev/null)
  if [ "$STATUS" = "Running" ]; then
    break
  fi
  WAIT_COUNT=$((WAIT_COUNT+1))
  if [ $WAIT_COUNT -gt 40 ]; then
    echo "[ERROR] Timed out waiting for Django pod."
    FAILED_STEPS+=("pod wait timeout")
    break
  fi
  echo "[INFO] Waiting for pod $DJANGO_POD to be Running..."
  sleep 3
  kubectl get pods || true
  kubectl get svc || true
  DJANGO_URL=$(minikube service django-service --url 2>/dev/null)
  echo "[INFO] Django service URL: $DJANGO_URL"
done

if [ "$STATUS" = "Running" ]; then
  echo "[INFO] Django pod is running: $DJANGO_POD"
  echo "[INFO] Running migrations in the Django pod..."
  kubectl exec -it "$DJANGO_POD" -- python manage.py migrate || FAILED_STEPS+=("migrate")
  echo "[INFO] Collecting static files in the Django pod..."
  kubectl exec -it "$DJANGO_POD" -- python manage.py collectstatic --noinput || FAILED_STEPS+=("collectstatic")
  echo "[INFO] Creating admin user in the Django pod..."
  kubectl exec -it "$DJANGO_POD" -- python manage.py create_admin || FAILED_STEPS+=("create_admin")
  echo "[INFO] Opening Django service in browser using minikube..."
  minikube service django-service || FAILED_STEPS+=("minikube service open")
  DJANGO_URL=$(minikube service django-service --url 2>/dev/null)
  echo "[INFO] Setup complete! Visit $DJANGO_URL in your browser."
else
  echo "[WARN] Skipping pod commands due to pod not running."
fi

echo "[INFO] To check status: kubectl get pods, kubectl get svc"
echo "[INFO] For troubleshooting and next steps, see README.md and KUBERNETES.md."

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