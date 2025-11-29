# AKS Deployment Guide

Complete guide for deploying Educated Guess to Azure Kubernetes Service.

## Prerequisites

- Azure subscription
- Azure CLI installed and configured
- kubectl installed
- Docker installed
- GitHub repository for CI/CD

## Step 1: Create Azure Resources

### 1.1 Create Resource Group
```bash
az group create \
  --name educated-guess-rg \
  --location eastus
```

### 1.2 Create Azure Container Registry (ACR)
```bash
az acr create \
  --resource-group educated-guess-rg \
  --name educatedguessacr \
  --sku Basic

# Enable admin access
az acr update -n educatedguessacr --admin-enabled true

# Get credentials
az acr credential show --name educatedguessacr
```

### 1.3 Create AKS Cluster
```bash
az aks create \
  --resource-group educated-guess-rg \
  --name educated-guess-aks \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --attach-acr educatedguessacr

# Get credentials
az aks get-credentials \
  --resource-group educated-guess-rg \
  --name educated-guess-aks
```

### 1.4 Create MongoDB VM
See [../infrastructure/vm/readme.md](../infrastructure/vm/readme.md) for detailed VM setup.

## Step 2: Install NGINX Ingress Controller

```bash
# Add Helm chart repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX ingress
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz
```

## Step 3: Configure Secrets and ConfigMaps

### 3.1 Create Kubernetes Secret
```bash
# Get MongoDB VM private IP
MONGO_VM_IP=$(az vm show -d -g educated-guess-rg -n mongodb-vm --query privateIps -o tsv)

# Create secret
kubectl create secret generic mongo-secret \
  --from-literal=mongodb_url="mongodb://app_user:YOUR_PASSWORD@${MONGO_VM_IP}:27017/educated_guess" \
  --from-literal=jwt_secret_key="your-secret-jwt-key-min-32-characters"
```

### 3.2 Apply ConfigMap
```bash
kubectl apply -f infrastructure/aks/deployment/configmap.yaml
```

### 3.3 Create ACR Secret for Image Pull
```bash
kubectl create secret docker-registry acr-secret \
  --docker-server=educatedguessacr.azurecr.io \
  --docker-username=educatedguessacr \
  --docker-password=<ACR_PASSWORD> \
  --docker-email=your@email.com
```

## Step 4: Build and Push Docker Images

### 4.1 Build Images
```bash
# Log in to ACR
az acr login --name educatedguessacr

# Build and tag frontend
docker build -t educatedguessacr.azurecr.io/educated-guess-frontend:latest ./frontend

# Build and tag backend
docker build -t educatedguessacr.azurecr.io/educated-guess-backend:latest ./backend
```

### 4.2 Push Images
```bash
docker push educatedguessacr.azurecr.io/educated-guess-frontend:latest
docker push educatedguessacr.azurecr.io/educated-guess-backend:latest
```

## Step 5: Deploy to AKS

### 5.1 Update Deployment YAML Files
Edit the following files and replace `<ACR_NAME>`:
- `infrastructure/aks/deployment/frontend-deployment.yaml`
- `infrastructure/aks/deployment/backend-deployment.yaml`

### 5.2 Apply Deployments
```bash
# Deploy backend
kubectl apply -f infrastructure/aks/deployment/backend-deployment.yaml
kubectl apply -f infrastructure/aks/service/backend-service.yaml

# Deploy frontend
kubectl apply -f infrastructure/aks/deployment/frontend-deployment.yaml
kubectl apply -f infrastructure/aks/service/frontend-service.yaml

# Deploy HPA
kubectl apply -f infrastructure/aks/deployment/hpa.yaml
```

### 5.3 Deploy Ingress
Update `infrastructure/aks/deployment/ingress.yaml` with your domain, then:
```bash
kubectl apply -f infrastructure/aks/deployment/ingress.yaml
```

## Step 6: Set Up DNS

### 6.1 Get Ingress External IP
```bash
kubectl get service -n ingress-nginx
```

### 6.2 Create DNS A Record
Point your domain (e.g., `educatedguess.example.com`) to the ingress external IP in your DNS provider.

## Step 7: Configure CI/CD

### 7.1 Create GitHub Secrets
In your GitHub repository, add these secrets:
- `ACR_USERNAME`: ACR admin username
- `ACR_PASSWORD`: ACR admin password
- `AZURE_CREDENTIALS`: Azure service principal JSON

To create Azure credentials:
```bash
az ad sp create-for-rbac \
  --name "educated-guess-github" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/educated-guess-rg \
  --sdk-auth
```

### 7.2 Copy CI/CD Workflows
```bash
mkdir -p .github/workflows
cp infrastructure/ci-cd/github-actions-frontend.yaml .github/workflows/
cp infrastructure/ci-cd/github-actions-backend.yaml .github/workflows/
```

## Step 8: Verify Deployment

### 8.1 Check Pods
```bash
kubectl get pods
kubectl logs -f deployment/backend-deployment
kubectl logs -f deployment/frontend-deployment
```

### 8.2 Check Services
```bash
kubectl get services
```

### 8.3 Check Ingress
```bash
kubectl get ingress
kubectl describe ingress educated-guess-ingress
```

### 8.4 Test Application
```bash
# Health check
curl http://YOUR_DOMAIN/api/health

# Frontend
curl http://YOUR_DOMAIN/
```

## Step 9: Enable HTTPS (Optional)

### 9.1 Install cert-manager
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml
```

### 9.2 Create ClusterIssuer
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your@email.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

```bash
kubectl apply -f clusterissuer.yaml
```

The ingress will automatically request a certificate.

## Monitoring and Maintenance

### View Logs
```bash
kubectl logs -f deployment/backend-deployment
kubectl logs -f deployment/frontend-deployment
```

### Scale Manually
```bash
kubectl scale deployment backend-deployment --replicas=5
```

### Update Application
```bash
# Build new image
docker build -t educatedguessacr.azurecr.io/educated-guess-backend:v2 ./backend
docker push educatedguessacr.azurecr.io/educated-guess-backend:v2

# Update deployment
kubectl set image deployment/backend-deployment \
  backend=educatedguessacr.azurecr.io/educated-guess-backend:v2

# Monitor rollout
kubectl rollout status deployment/backend-deployment
```

### Rollback
```bash
kubectl rollout undo deployment/backend-deployment
```

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Cannot connect to MongoDB
```bash
# Test from a pod
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
# Inside pod:
telnet <MONGO_VM_IP> 27017
```

### Ingress not working
```bash
kubectl describe ingress educated-guess-ingress
kubectl get service -n ingress-nginx
```

## Cost Optimization

### Use Azure Spot VMs
```bash
az aks nodepool add \
  --resource-group educated-guess-rg \
  --cluster-name educated-guess-aks \
  --name spotnodes \
  --priority Spot \
  --eviction-policy Delete \
  --spot-max-price -1 \
  --node-count 2
```

### Stop AKS during non-business hours
```bash
az aks stop --name educated-guess-aks --resource-group educated-guess-rg
az aks start --name educated-guess-aks --resource-group educated-guess-rg
```

## Security Best Practices

1. ✅ Use private ACR
2. ✅ Enable RBAC on AKS
3. ✅ Use Azure Key Vault for secrets
4. ✅ Enable Azure Policy
5. ✅ Regular security updates
6. ✅ Network policies
7. ✅ Pod security policies
8. ✅ Azure Defender for Kubernetes
