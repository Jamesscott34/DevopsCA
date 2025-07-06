# 🚢 Helm Deployment Guide for SBA24070 Book Catalogue App

This guide explains how to deploy the Book Catalogue App to Kubernetes using the provided Helm chart in the `book-catalogue/` directory.

---

## Prerequisites
- A running Kubernetes cluster (local: minikube/kind, or cloud: GKE, EKS, AKS, etc.)
- [Helm 3+](https://helm.sh/) installed on your machine
- Docker image for the app (build and push to a registry if customizing)

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

## Chart Directory Structure
- `Chart.yaml` — Chart metadata
- `values.yaml` — Default configuration values
- `templates/` — Kubernetes resource templates (Deployment, Service, Ingress, etc.)
- `charts/` — (Optional) Subcharts/dependencies
- `.helmignore` — Files to ignore when packaging the chart

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

## Notes
- Make sure your database (e.g., PostgreSQL) is accessible from the cluster, or deploy it as part of your stack.
- For production, set up persistent storage and secrets for sensitive data.
- You can use Helm's upgrade and rollback features for safe deployments.

---

For more details, see the [Helm documentation](https://helm.sh/docs/). 