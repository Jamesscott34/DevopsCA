# 🚦 What To Do Next: Kubernetes Deployment Checklist

1. **Stop any local Docker containers**
   - `docker-compose down` or `docker stop $(docker ps -q)`

2. **Push your Docker image to Docker Hub**
   - `docker build -t jamesdeanscott/devops-book-app:latest .`
   - `docker push jamesdeanscott/devops-book-app:latest`

3. **Apply Kubernetes manifests (in order):**
   ```sh
   kubectl apply -f k8s/secret.yaml
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/postgres-deployment.yaml
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. **Check resources:**
   - `kubectl get pods`
   - `kubectl get svc`
   - `kubectl get deployments`

5. **Access your app:**
   - For NodePort: `kubectl get svc django-service` and visit `http://<node-ip>:<node-port>`
   - For port-forward: `kubectl port-forward service/django-service 8000:80` and visit [http://localhost:8000](http://localhost:8000)

6. **Troubleshooting:**
   - Use `kubectl logs <pod-name>` for logs
   - Use `kubectl describe pod <pod-name>` for details
   - Check for port conflicts or image pull errors

7. **Security Reminder:**
   - Never commit real secrets to public repositories!
   - Use `.gitignore` to exclude `k8s/secret.yaml` and other sensitive files.

---

For more, see the main `README.md` and your Helm chart documentation. 