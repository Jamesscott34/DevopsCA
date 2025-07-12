# 📚 SBA24070 Book Catalogue App

**Welcome!** This app is a full-featured Django book catalogue with flexible deployment: local, Docker, Kubernetes, and Helm. This README will guide you from zero to production, including troubleshooting and automation scripts.

**Database Flexibility Note:**
- By default, the app uses SQLite, which requires no setup just clone and run.
- You can switch to PostgreSQL (or another supported DB) by updating `settings.py` (or your `.env` for Docker) and running migrations.
- See [Quickstart Guide](docs/QUICKSTART.md) for setup instructions for both local and Docker environments.

You can use the provided scripts for setup:
- `custom_scripts/run_django.sh`: Local Django setup
- `custom_scripts/run_docker.sh`: Docker Compose setup
- `custom_scripts/setup.sh`: Interactive setup for both modes and kubernets installation

---

## 🚦 Quick Start

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
- See [KUBERNETES.md](KUBERNETES.md) for advanced/manual steps.

### 4. Helm Chart
- See [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md) for Helm-based deployment and customization.

---

## 🛠️ Helper & Management Scripts

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

## 🧑‍💻 Admin & User Management

- Admin user: `admin` / `admin` (created automatically by scripts)
- Use `custom_scripts/admin_manager.py` to manage admin user and view user stats.
- Admin dashboard: `/admin-dashboard/`
- User dashboard: `/home/`

---

## 🔗 Documentation
- [Quickstart Guide](docs/QUICKSTART.md)
- [Kubernetes Guide](docs/KUBERNETES.md)
- [Helm Deployment](docs/HELM_DEPLOYMENT.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [API Example (JavaScript)](static/js/api-example.js)

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

## 📝 Contributing
- Fork the repo, create a branch, and submit a PR.
- Please update documentation for any new features or changes.

---

## 🛠️ Tech Stack
- **Backend**: Django (Python 3.8+)
- **Database**: SQLite (default), PostgreSQL ready
- **Frontend**: HTML + Bootstrap + Custom CSS
- **External API**: [Open Library](https://openlibrary.org/developers/api)
- **Version Control**: Git + GitHub
- **Authentication**: Custom user model with password hashing

---

## 👨‍💻 Author
**James Scott**  
Student ID: SBA24070  
Email: jamesdeanscott19@gmail.com  
GitHub: [github.com/Jamesscott34](https://github.com/Jamesscott34)

---

## 🚀 How It Works
- **Login Page** is the default landing page.
- **User Registration** for new users.
- **Home Page** shows your saved books and reading progress.
- **Manual Add**: Enter book details and auto-generate ISBN.
- **Open Library Search**: Search/import books from Open Library.
- **Admin Dashboard**: Admin can view/manage users, see stats, view any user's books, and set referral books.
- **Books**: Edit, delete, mark read/unread.
- **Notifications**: Admins can send messages and book recommendations.
- **User/Admin Book Separation**: Users and admin see only their own books on `/home/`. Admin can view any user's books from the dashboard.
- **Admin Referral Feature**: Admin can set a referral book for any user; users can add the referral to their collection from their profile.
- **User Notes**: Users can add/edit personal notes in their profile.

---

## ✅ Features So Far
- [x] Login Page as Default Landing Page
- [x] Manual Book Entry Form with Description and JS-ISBN
- [x] Editable Book Entries
- [x] Delete and Toggle Status
- [x] Open Library Integration with Search + Import
- [x] Book Table with Description Column
- [x] Bootstrap Styling with Custom Color Theme
- [x] User Registration (Sign Up)
- [x] User Login/Logout with Session Management
- [x] Personalized Welcome Message
- [x] Admin User and Dashboard
- [x] Admin User Management Script
- [x] User Deletion from Admin Dashboard
- [x] User Profile Editing and Password Reset
- [x] Profile Deletion with Confirmation
- [x] Comprehensive Notification System
- [x] Book Statistics and Reading Progress Tracking
- [x] Admin Restrictions (can only change own email, cannot notify self)
- [x] Book View Tracking and Attribution
- [x] Automatic Book Saving from Notifications
- [x] Complete REST API with Authentication, CRUD Operations, and Statistics
- [x] Add search and filter options to local book list
- [x] Improve validation and error handling
- [x] Implement cover image upload for manually added books
- [x] Add book categories and tags
- [x] User/admin book separation (users and admin see only their own books on `/home/`)
- [x] Admin can view any user's books from the admin dashboard
- [x] Admin referral feature: admin can set a referral book for any user, and users can add it to their collection
- [x] User notes: users can add/edit personal notes in their profile
- [x] Kubernetes deployment with full automation (setup.sh)

---

## 🚧 Planned Features
- Email notification functionality
- Book import/export (CSV, JSON)
- Analytics/dashboard for users (reading stats, most read authors, etc.)
- Enhanced book cover image support (drag-and-drop, cropping)
- User profile picture/avatar
- Improved mobile responsiveness and accessibility
- Ingress and HTTPS for Kubernetes
- Advanced tags/categories and filtering
- Reading streak tracker
- Smart book recommendations (NLTK, spaCy, or keyword matching)
- Book stats graphs (matplotlib, plotly, Chart.js)
- Calendar view for reading log
- Automated API tests (pytest, unittest, django.test.TestCase)
- CI/CD pipeline for automated testing, building, and deployment
- Book analytics, profile pictures, mobile improvements
- Helm chart improvements and versioning

---

## 🚀 Kubernetes Deployment

- The `setup.sh` script now fully automates Kubernetes onboarding:
  - Applies all manifests
  - Waits for the Django pod to be ready
  - Runs migrations, collects static files, and creates the admin user in the pod
  - Opens the Django service in your browser (via minikube)
  - Uses `curl` to test the service URL as your user
- No manual pod/command steps needed—just follow the prompts!

See [KUBERNETES.md](KUBERNETES.md) for a complete, step-by-step guide to deploying this app on Kubernetes. This includes preparing secrets, applying manifests, and accessing the app.

## 🐳 Docker Hub & GitHub Actions Setup

To use CI/CD and automatic Docker image builds, you must:

1. **Create a Docker Hub account** (https://hub.docker.com/)
2. **Create a Docker repository** (e.g., `yourusername/devops-book-app`)
3. **Add your Docker Hub credentials to your GitHub repository secrets:**
   - Go to your repo on GitHub → Settings → Secrets and variables → Actions → New repository secret
   - Add:
     - `DOCKER_USERNAME` (your Docker Hub username)
     - `DOCKER_PASSWORD` (your Docker Hub password or access token)
4. **Update your workflow and manifests to use your Docker Hub image name.**

**You will be prompted for your Docker Hub username in the setup script.**

See [KUBERNETES.md](KUBERNETES.md) for Kubernetes deployment, and the GitHub Actions workflow for CI/CD details.

---

## ✅ REST API
A complete REST API is available for integration with JavaScript frontends, mobile apps, and other services. See [API Documentation](API_DOCUMENTATION.md) for all endpoints, authentication, and usage examples.

---

## 📋 Notification System Support

For issues and questions:
1. Check the troubleshooting section
2. Review the admin management script documentation
3. Check Django documentation for framework-specific issues

---

## 🏁 After Setup: Running Your App on Minikube

1. **Start Minikube:**
   ```sh
   minikube start
   ```

2. **Find the Django Service URL:**
   ```sh
   minikube service django-service
   ```
   This will open your Django app in your browser. If not, note the URL and port (e.g., `http://<minikube-ip>:<nodeport>`).

3. **Run Django Management Commands in the Pod:**
   First, get the name of your Django pod:
   ```sh
   kubectl get pods
   ```
   (Look for a pod name starting with `django-deployment-`)

   Then run the following commands (replace `<pod-name>` with your actual pod name):

   - **Migrate the database:**
     ```sh
     kubectl exec -it <pod-name> -- python manage.py migrate
     ```
   - **Collect static files:**
     ```sh
     kubectl exec -it <pod-name> -- python manage.py collectstatic --noinput
     ```
   - **Create admin user:**
     ```sh
     kubectl exec -it <pod-name> -- python manage.py createsuperuser
     ```

---

## 🗄️ Switching Database Host for Local vs Docker/Kubernetes

- By default, Django uses the environment variable POSTGRES_HOST for the database host, defaulting to 'db'.
- For **local development** (when running `python manage.py runserver`), you should set the default to 'localhost' in your `settings.py`:
  ```python
  'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
  ```
- For **Docker, Docker Compose, or Kubernetes**, set the default to 'db':
  ```python
  'HOST': os.environ.get('POSTGRES_HOST', 'db'),
  ```
- You can automate this update by running a helper script (custom_scripts/host_helper.py) that will prompt you to choose the correct default and update your `settings.py` automatically.

**Tip:** Always use the environment variable POSTGRES_HOST in your deployment environments for maximum flexibility.

---
