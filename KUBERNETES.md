# 🚀 Kubernetes Quick Start Guide

Welcome! This guide will help you deploy the Book Catalogue App on Kubernetes, with step-by-step instructions for Minikube and generic clusters.

---

## Prerequisites
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- `kubectl` installed and configured
- Docker image available at `jamesdeanscott/devops-book-app:latest` (already pushed)
- [Optional] [Helm 3+](https://helm.sh/) for Helm-based deployment (see [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md))

---

## 1. Clone the Repository
```sh
git clone https://github.com/Jamesscott34/DevopsCA.git
cd DevopsCA
```

---

## 2. Prepare Your Secrets & Configs
- Copy the example secret and fill in your own base64-encoded values:
  ```sh
  cp k8s/secret.example.yaml k8s/secret.yaml
  # Edit k8s/secret.yaml and replace the dummy values with your own (base64-encoded)
  ```
- **Never commit real secrets to public repositories!**
- You can also use `./setup.sh` to generate secrets and configs interactively.

---

## 3. Apply Kubernetes Manifests
All manifests are in the `k8s/` directory. Apply them in this order:
```sh
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

---

## 4. Access the App
- Get the NodePort for the Django service:
  ```sh
  kubectl get svc django-service
  ```
- Visit `http://<node-ip>:<node-port>` in your browser.
  - For Minikube: `minikube ip` gives the node IP.
  - For Docker Desktop: use `localhost` and the NodePort.
  - Or use: `minikube service django-service` to open in your browser.

---

## 5. Post-Deployment: Migrations, Static Files, Admin

After your pods are running, initialize the database and static files:

1. **Get the Django pod name:**
   ```sh
   kubectl get pods
   # Or:
   DJANGO_POD=$(kubectl get pods -l app=django -o jsonpath='{.items[0].metadata.name}')
   ```
2. **Run migrations:**
   ```sh
   kubectl exec -it $DJANGO_POD -- python manage.py migrate
   ```
3. **Collect static files:**
   ```sh
   kubectl exec -it $DJANGO_POD -- python manage.py collectstatic --noinput
   ```
4. **Create admin user:**
   ```sh
   kubectl exec -it $DJANGO_POD -- python manage.py create_admin
   ```

---

## 6. Automation: Use setup.sh

- The `setup.sh` script automates all the above steps:
  - Prompts for secrets/configs
  - Applies manifests
  - Waits for pods
  - Runs migrations, collects static, creates admin
  - Opens the Django service in your browser
- Just run:
  ```sh
  ./setup.sh
  ```

---

## 7. Troubleshooting & FAQ

- **Pods not starting:**
  - Check pod logs: `kubectl logs <pod-name>`
  - Ensure secrets/configs are correct and applied
- **Database connection errors:**
  - Make sure Postgres pod is running and accessible
  - Check DB host in your environment/configs (should be `db` or `postgres`)
- **Admin login fails:**
  - Use `kubectl exec -it $DJANGO_POD -- python admin_manager.py reset` to reset admin password
- **Resetting/cleaning:**
  - Remove all resources: `kubectl delete -f k8s/`
  - Re-run `./setup.sh` to redeploy

---

## 8. See Also
- [README.md](README.md) for full onboarding and troubleshooting
- [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md) for Helm-based deployment
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API usage

---

**Tip:** For most users, `./setup.sh` is the fastest way to get started! 