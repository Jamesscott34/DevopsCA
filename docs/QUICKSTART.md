# SBA24070 Book Catalogue App – Quickstart

This guide will help you get started with the Book Catalogue App in any environment: local, Docker, or Kubernetes. For full details, see [README.md](../README.md).

---

## 🚦 Quick Start Options

### 1. Local Development (SQLite, no setup required)
```sh
custom_scripts/run_django.sh
```
- Installs dependencies, runs migrations, creates admin, and starts the server.
- Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Admin login: `admin` / `admin`

### 2. Docker Compose (Postgres, for local containers)
```sh
custom_scripts/run_docker.sh
```
- Builds and starts containers, runs migrations, collects static, creates admin.
- Visit: [http://localhost:8000](http://localhost:8000)
- Admin login: `admin` / `admin`

### 3. Kubernetes (Minikube or any cluster)
```sh
custom_scripts/setup.sh
```
- Fully interactive: prompts for secrets, creates .env and k8s secrets, applies manifests, waits for pods, runs migrations, creates admin, opens browser.
- See [docs/KUBERNETES.md](docs/KUBERNETES.md) for advanced/manual steps.

---

## 🛠️ Helper Scripts
- `custom_scripts/run_django.sh`: Local dev setup (uses SQLite or local Postgres)
- `custom_scripts/run_docker.sh`: Docker Compose setup (uses Postgres service)
- `custom_scripts/setup.sh`: Full onboarding for all environments (local, Docker, Kubernetes)
- `custom_scripts/host_helper.py`: Interactively set the default DB host in `settings.py` (choose 'localhost' or 'db')
- `custom_scripts/admin_manager.py`: Create, verify, reset, and show stats for the admin user. Usage:
  - `python custom_scripts/admin_manager.py` (full setup)
  - `python custom_scripts/admin_manager.py create|verify|test|stats|reset`

---

## 🗄️ Environment Variables & Database Host
- The app uses environment variables for all secrets and DB config.
- For **local dev**, DB host should be `localhost`.
- For **Docker/Kubernetes**, DB host should be `db` (or the service name).
- Use `custom_scripts/host_helper.py` to switch the default in `settings.py`.
- Always set `POSTGRES_HOST` in your deployment environments for flexibility.

---

## 🐞 Troubleshooting & FAQ
- **Database connection errors:**
  - Check your DB host in `settings.py` and environment variables.
  - Use `custom_scripts/host_helper.py` to set the correct default.
  - For Docker/K8s, ensure the Postgres service is running and accessible.
- **Migrations not applied:**
  - Run the migration commands in the appropriate environment (see above).
- **Admin login fails:**
  - Use `custom_scripts/admin_manager.py reset` to reset the admin password to `admin`.
- **Pods not starting (Kubernetes):**
  - Check pod logs: `kubectl logs <pod-name>`
  - Ensure secrets/configs are set up (see `custom_scripts/setup.sh` and `docs/KUBERNETES.md`).
- **Resetting the environment:**
  - Local: Remove `devops/`, `db.sqlite3`, and re-run `custom_scripts/run_django.sh`.
  - Docker: `docker compose down -v` to remove containers and volumes, then run `custom_scripts/run_docker.sh`.
  - Kubernetes: `kubectl delete -f k8s/` to remove all resources, then run `custom_scripts/setup.sh`.

---

## 🧹 Reset/Clean Instructions
- **Local:**
  ```sh
  rm -rf devops/ db.sqlite3
  custom_scripts/run_django.sh
  ```
- **Docker:**
  ```sh
  docker compose down -v
  custom_scripts/run_docker.sh
  ```
- **Kubernetes:**
  ```sh
  kubectl delete -f k8s/
  custom_scripts/setup.sh
  ```

---

## 🔗 More Documentation
- [README.md](../README.md) (full onboarding, troubleshooting, and advanced usage)
- [docs/KUBERNETES.md](docs/KUBERNETES.md) (Kubernetes deployment)
- [docs/HELM_DEPLOYMENT.md](docs/HELM_DEPLOYMENT.md) (Helm deployment)
- [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) (API usage) 