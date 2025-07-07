# 🚀 Kubernetes Quick Start Guide

Welcome! This guide will help you deploy the Book Catalogue App on Kubernetes.

## Prerequisites
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- `kubectl` installed and configured
- Docker image available at `jamesdeanscott/devops-book-app:latest` (already pushed)

## 1. Clone the Repository
```sh
git clone https://github.com/Jamesscott34/DevopsCA.git
cd DevopsCA
```

## 2. Prepare Your Secrets
- Copy the example secret and fill in your own base64-encoded values:
  ```sh
  cp k8s/secret.example.yaml k8s/secret.yaml
  # Edit k8s/secret.yaml and replace the dummy values with your own (base64-encoded)
  ```
- **Never commit real secrets to public repositories!**

## 3. Apply Kubernetes Manifests
All manifests are in the `k8s/` directory. Apply them in this order:
```sh
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## 4. Access the App
- Get the NodePort for the Django service:
  ```sh
  kubectl get svc django-service
  ```
- Visit `http://<node-ip>:<node-port>` in your browser.
  - For Minikube: `minikube ip` gives the node IP.
  - For Docker Desktop: use `localhost` and the NodePort.

## 5. Stopping/Restarting
- To stop: `kubectl delete -f k8s/`
- To restart: re-apply the manifests as above.

---
For advanced usage (Helm, CI/CD, etc.), see the main `README.md`. 