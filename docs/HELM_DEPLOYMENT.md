# 🚢 Helm Deployment Guide for SBA24070 Book Catalogue App

This guide explains how to deploy the Book Catalogue App to Kubernetes using the provided Helm chart in the `book-catalogue/` directory. Helm makes it easy to install, upgrade, and manage your deployment.

---

## Prerequisites
- A running Kubernetes cluster (local: minikube/kind, or cloud: GKE, EKS, AKS, etc.)
- [Helm 3+](https://helm.sh/) installed on your machine
- Docker image for the app (build and push to a registry if customizing)
- Kubernetes secrets and configs prepared (see [KUBERNETES.md](KUBERNETES.md) or use `setup.sh`)

---

## Chart Location
- The Helm chart is in the [`book-catalogue/`](./book-catalogue/) directory of this repository.

---

## Basic Usage

### 1. Install the app
```sh
helm install my-book-app ./book-catalogue
```

### 2. Upgrade the app
```sh
helm upgrade my-book-app ./book-catalogue
```

### 3. Uninstall the app
```sh
helm uninstall my-book-app
```

---

## Customizing Your Deployment

You can customize your deployment by editing `book-catalogue/values.yaml` or by providing your own values file:

```sh
helm install my-book-app ./book-catalogue -f my-values.yaml
```

Common settings to override:
- `image.repository` and `image.tag` (if using your own Docker image)
- `env` (environment variables, e.g., database credentials)
- `service.type` and `service.port`
- `ingress.enabled` and related settings (if exposing via Ingress)

See all available options in [`book-catalogue/values.yaml`](./book-catalogue/values.yaml).

---

## Example: Custom Values File

Create a file called `my-values.yaml`:
```yaml
image:
  repository: your-docker-repo/book-catalogue
  tag: latest
service:
  type: LoadBalancer
  port: 8000
env:
  DJANGO_SETTINGS_MODULE: sba24070_book_catalogue.settings
  # Add other environment variables as needed
```
Then install with:
```sh
helm install my-book-app ./book-catalogue -f my-values.yaml
```

---

## Automation & Integration
- You can use `setup.sh` to prepare secrets/configs before deploying with Helm.
- Helm can be used as an alternative to manual `kubectl apply` or as part of your CI/CD pipeline.
- For advanced automation, see [KUBERNETES.md](KUBERNETES.md) and [README.md](README.md).

---

## Troubleshooting & FAQ
- **Pods not starting:**
  - Check pod logs: `kubectl logs <pod-name>`
  - Ensure secrets/configs are correct and applied
- **Database connection errors:**
  - Make sure Postgres is running and accessible
  - Check DB host in your values/configs (should be `db` or `postgres`)
- **Admin login fails:**
  - Use `kubectl exec -it <django-pod> -- python admin_manager.py reset` to reset admin password
- **Resetting/cleaning:**
  - Uninstall the release: `helm uninstall my-book-app`
  - Remove persistent volumes if needed

---

## See Also
- [README.md](README.md) for full onboarding and troubleshooting
- [KUBERNETES.md](KUBERNETES.md) for manual/automated Kubernetes deployment
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API usage

---

**Tip:** Helm is ideal for production and repeatable deployments. For first-time users, try `setup.sh` or manual steps first, then use Helm for upgrades and scaling! 