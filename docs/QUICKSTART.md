# SBA24070 Book Catalogue App – Quickstart

This guide will help you get started with the Book Catalogue App in any environment: local, Docker, or Kubernetes. For full details, see [README.md](../README.md).

---

## 🚦 Quick Start Options

### 1. Local Development (SQLite, no setup required)
```sh
./run_django.sh
```
- Installs dependencies, runs migrations, creates admin, and starts the server.
- Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Admin login: `admin` / `admin`

### 2. Docker Compose (Postgres, for local containers)
```sh
./run_docker.sh
```
- Builds and starts containers, runs migrations, collects static, creates admin.
- Visit: [http://localhost:8000](http://localhost:8000)
- Admin login: `admin` / `admin`

### 3. Kubernetes (Minikube or any cluster)
```sh
./setup.sh
```
- Fully interactive: prompts for secrets, creates .env and k8s secrets, applies manifests, waits for pods, runs migrations, creates admin, opens browser.
- See [KUBERNETES.md](../KUBERNETES.md) for advanced/manual steps.

---

## 🛠️ Helper Scripts
- `run_django.sh`: Local dev setup (uses SQLite or local Postgres)
- `run_docker.sh`: Docker Compose setup (uses Postgres service)
- `setup.sh`: Full onboarding for all environments (local, Docker, Kubernetes)
- `host_helper.py`: Interactively set the default DB host in `settings.py` (choose 'localhost' or 'db')
- `admin_manager.py`: Create, verify, reset, and show stats for the admin user. Usage:
  - `python admin_manager.py` (full setup)
  - `python admin_manager.py create|verify|test|stats|reset`

---

## 🗄️ Environment Variables & Database Host
- The app uses environment variables for all secrets and DB config.
- For **local dev**, DB host should be `localhost`.
- For **Docker/Kubernetes**, DB host should be `db` (or the service name).
- Use `host_helper.py` to switch the default in `settings.py`.
- Always set `POSTGRES_HOST` in your deployment environments for flexibility.

---

## 🐞 Troubleshooting & FAQ
- **Database connection errors:**
  - Check your DB host in `settings.py` and environment variables.
  - Use `host_helper.py` to set the correct default.
  - For Docker/K8s, ensure the Postgres service is running and accessible.
- **Migrations not applied:**
  - Run the migration commands in the appropriate environment (see above).
- **Admin login fails:**
  - Use `admin_manager.py reset` to reset the admin password to `admin`.
- **Pods not starting (Kubernetes):**
  - Check pod logs: `kubectl logs <pod-name>`
  - Ensure secrets/configs are set up (see `setup.sh` and `KUBERNETES.md`).
- **Resetting the environment:**
  - Local: Remove `devops/`, `db.sqlite3`, and re-run `run_django.sh`.
  - Docker: `docker compose down -v` to remove containers and volumes.
  - Kubernetes: `kubectl delete -f k8s/` to remove all resources.

---

## 🧹 Reset/Clean Instructions
- **Local:**
  ```sh
  rm -rf devops/ db.sqlite3
  ./run_django.sh
  ```
- **Docker:**
  ```sh
  docker compose down -v
  ./run_docker.sh
  ```
- **Kubernetes:**
  ```sh
  kubectl delete -f k8s/
  ./setup.sh
  ```

---

## 🔗 More Documentation
- [README.md](../README.md) (full onboarding, troubleshooting, and advanced usage)
- [KUBERNETES.md](../KUBERNETES.md) (Kubernetes deployment)
- [HELM_DEPLOYMENT.md](../HELM_DEPLOYMENT.md) (Helm deployment)
- [API_DOCUMENTATION.md](../API_DOCUMENTATION.md) (API usage) 