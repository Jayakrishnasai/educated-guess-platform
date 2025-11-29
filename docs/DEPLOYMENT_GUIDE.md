# 🚀 Educated Guess - Complete Deployment Guide

> **For DevOps Beginners**: This guide will walk you through deploying a three-tier application to Azure step-by-step.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Azure Setup](#phase-1-azure-setup)
4. [Phase 2: MongoDB VM Setup](#phase-2-mongodb-vm-setup)
5. [Phase 3: Azure Kubernetes Service (AKS) Setup](#phase-3-azure-kubernetes-service-aks-setup)
6. [Phase 4: Container Registry Setup](#phase-4-container-registry-setup)
7. [Phase 5: Application Deployment](#phase-5-application-deployment)
8. [Phase 6: CI/CD Pipeline Setup](#phase-6-cicd-pipeline-setup)
9. [Phase 7: Verification & Testing](#phase-7-verification--testing)
10. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```mermaid
graph TB
    subgraph "Users"
        U[Web Browser]
    end
    
    subgraph "Azure Kubernetes Service (AKS)"
        subgraph "Frontend Pods"
            F1[React App 1]
            F2[React App 2]
        end
        subgraph "Backend Pods"
            B1[FastAPI 1]
            B2[FastAPI 2]
        end
        LB[Load Balancer]
    end
    
    subgraph "Azure VM"
        DB[(MongoDB)]
    end
    
    subgraph "Azure Container Registry"
        ACR[Container Images]
    end
    
    subgraph "GitHub"
        GH[GitHub Actions CI/CD]
    end
    
    U --> LB
    LB --> F1
    LB --> F2
    F1 --> B1
    F2 --> B2
    B1 --> DB
    B2 --> DB
    GH --> ACR
    ACR --> F1
    ACR --> F2
    ACR --> B1
    ACR --> B2
```

**Three Tiers:**
- **Tier 1 (Frontend)**: React application running in AKS
- **Tier 2 (Backend)**: FastAPI application running in AKS
- **Tier 3 (Database)**: MongoDB running on a dedicated Azure VM

---

## Prerequisites

### Required Accounts & Tools

#### 1. Azure Account
- Create a free account at [portal.azure.com](https://portal.azure.com)
- You'll get $200 credit for 30 days (enough for this deployment)

#### 2. GitHub Account
- Create account at [github.com](https://github.com)
- You'll use this for CI/CD pipelines

#### 3. Install Required Tools

**On Windows (PowerShell as Administrator):**

```powershell
# Install Chocolatey (package manager)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install Azure CLI
choco install azure-cli -y

# Install kubectl (Kubernetes CLI)
choco install kubernetes-cli -y

# Install Git
choco install git -y

# Verify installations
az --version
kubectl version --client
git --version
```

---

## Phase 1: Azure Setup

### Step 1.1: Login to Azure

```bash
# Login to Azure account
az login

# This will open a browser window - login with your Azure credentials

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "YOUR-SUBSCRIPTION-NAME"
```

### Step 1.2: Create Resource Group

A **Resource Group** is a container that holds related Azure resources.

```bash
# Choose a region close to you:
# - eastus (US East Coast)
# - westus2 (US West Coast)
# - westeurope (Europe)
# - southeastasia (Asia)

az group create \
  --name educated-guess-rg \
  --location eastus

# Expected output: "provisioningState": "Succeeded"
```

**What this does:** Creates a logical container for all your Azure resources.

---

## Phase 2: MongoDB VM Setup

### Step 2.1: Create Virtual Network

A **Virtual Network** allows your resources to communicate securely.

```bash
az network vnet create \
  --resource-group educated-guess-rg \
  --name educated-guess-vnet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name database-subnet \
  --subnet-prefix 10.0.1.0/24
```

### Step 2.2: Create Network Security Group (Firewall)

```bash
# Create NSG
az network nsg create \
  --resource-group educated-guess-rg \
  --name mongodb-nsg

# Allow SSH (port 22) for remote access
az network nsg rule create \
  --resource-group educated-guess-rg \
  --nsg-name mongodb-nsg \
  --name AllowSSH \
  --priority 1000 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-port-ranges 22 \
  --protocol Tcp \
  --access Allow

# Allow MongoDB (port 27017) from AKS subnet only
az network nsg rule create \
  --resource-group educated-guess-rg \
  --nsg-name mongodb-nsg \
  --name AllowMongoDB \
  --priority 1001 \
  --source-address-prefixes 10.0.2.0/24 \
  --source-port-ranges '*' \
  --destination-port-ranges 27017 \
  --protocol Tcp \
  --access Allow
```

### Step 2.3: Create MongoDB VM

```bash
# Create Ubuntu VM for MongoDB
az vm create \
  --resource-group educated-guess-rg \
  --name mongodb-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --vnet-name educated-guess-vnet \
  --subnet database-subnet \
  --nsg mongodb-nsg \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Save the output - you'll need the publicIpAddress!
```

> 💡 **Note:** Save the `publicIpAddress` from the output. You'll need it to connect via SSH.

### Step 2.4: Install MongoDB on VM

```bash
# Get your VM's public IP
VM_IP=$(az vm show -d \
  --resource-group educated-guess-rg \
  --name mongodb-vm \
  --query publicIps -o tsv)

echo "Your VM IP: $VM_IP"

# SSH into the VM
ssh azureuser@$VM_IP
```

Once connected to the VM, run:

```bash
# Download the MongoDB installation script from your project
# First, exit SSH and from your local machine, copy the script:
exit

# Copy the installation script to the VM
scp infrastructure/vm/mongodb-install.sh azureuser@$VM_IP:~/

# SSH back into the VM
ssh azureuser@$VM_IP

# Run the installation script
sudo bash mongodb-install.sh
```

### Step 2.5: Configure MongoDB Users

After installation, create database users:

```bash
# Connect to MongoDB shell
mongosh

# Switch to admin database
use admin

# Create admin user
db.createUser({
  user: "admin",
  pwd: "YOUR_STRONG_PASSWORD_HERE",
  roles: ["root"]
})

# Exit and reconnect with authentication
exit
mongosh -u admin -p

# Create application user
use educated_guess

db.createUser({
  user: "app_user",
  pwd: "YOUR_APP_PASSWORD_HERE",
  roles: [
    { role: "readWrite", db: "educated_guess" }
  ]
})

exit
```

> 🔒 **Security Tip:** Use strong passwords! Consider using a password generator.

### Step 2.6: Get VM Private IP

```bash
# Exit from VM
exit

# Get the private IP (needed for AKS to connect)
VM_PRIVATE_IP=$(az vm show -d \
  --resource-group educated-guess-rg \
  --name mongodb-vm \
  --query privateIps -o tsv)

echo "MongoDB Private IP: $VM_PRIVATE_IP"
# Save this IP - you'll use it in Kubernetes secrets
```

---

## Phase 3: Azure Kubernetes Service (AKS) Setup

### Step 3.1: Create AKS Subnet

```bash
az network vnet subnet create \
  --resource-group educated-guess-rg \
  --vnet-name educated-guess-vnet \
  --name aks-subnet \
  --address-prefix 10.0.2.0/24
```

### Step 3.2: Create AKS Cluster

> ⏱️ **Note:** This step takes 5-10 minutes

```bash
az aks create \
  --resource-group educated-guess-rg \
  --name educated-guess-aks \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --vnet-subnet-id /subscriptions/$(az account show --query id -o tsv)/resourceGroups/educated-guess-rg/providers/Microsoft.Network/virtualNetworks/educated-guess-vnet/subnets/aks-subnet \
  --enable-managed-identity \
  --generate-ssh-keys \
  --network-plugin azure

# Wait for "provisioningState": "Succeeded"
```

**What this creates:**
- 2 Virtual Machines to run your containers
- Load balancer for distributing traffic
- Managed Kubernetes control plane

### Step 3.3: Connect to AKS Cluster

```bash
# Download credentials to use kubectl
az aks get-credentials \
  --resource-group educated-guess-rg \
  --name educated-guess-aks

# Verify connection
kubectl get nodes

# You should see 2 nodes in "Ready" status
```

---

## Phase 4: Container Registry Setup

### Step 4.1: Create Azure Container Registry (ACR)

ACR stores your Docker images (like Docker Hub, but private).

```bash
# Registry names must be globally unique and lowercase
az acr create \
  --resource-group educated-guess-rg \
  --name educatedguessacr \
  --sku Basic

# Expected output: "provisioningState": "Succeeded"
```

### Step 4.2: Connect AKS to ACR

Allow AKS to pull images from ACR:

```bash
az aks update \
  --resource-group educated-guess-rg \
  --name educated-guess-aks \
  --attach-acr educatedguessacr
```

### Step 4.3: Enable Admin Access (for CI/CD)

```bash
az acr update \
  --name educatedguessacr \
  --admin-enabled true

# Get credentials (save these for GitHub Secrets)
az acr credential show \
  --name educatedguessacr
```

> 📝 **Save these credentials:** You'll need `username` and `passwords[0].value` for GitHub Actions.

---

## Phase 5: Application Deployment

### Step 5.1: Create Kubernetes Secrets

Secrets store sensitive data like passwords and connection strings.

```bash
# Create namespace
kubectl create namespace educated-guess

# Create MongoDB connection secret
# Replace VM_PRIVATE_IP and YOUR_APP_PASSWORD with actual values
kubectl create secret generic mongo-secret \
  --from-literal=mongodb-url="mongodb://app_user:YOUR_APP_PASSWORD@VM_PRIVATE_IP:27017/educated_guess?authSource=educated_guess" \
  --namespace educated-guess

# Create JWT secret for backend
kubectl create secret generic jwt-secret \
  --from-literal=secret-key="$(openssl rand -base64 32)" \
  --namespace educated-guess

# Verify secrets were created
kubectl get secrets -n educated-guess
```

### Step 5.2: Build and Push Docker Images

#### Build Backend Image

```bash
# Navigate to backend directory
cd backend

# Login to ACR
az acr login --name educatedguessacr

# Build and push backend image
docker build -t educatedguessacr.azurecr.io/educated-guess-backend:v1 .
docker push educatedguessacr.azurecr.io/educated-guess-backend:v1

cd ..
```

#### Build Frontend Image

```bash
# Navigate to frontend directory
cd frontend

# Build and push frontend image
docker build -t educatedguessacr.azurecr.io/educated-guess-frontend:v1 .
docker push educatedguessacr.azurecr.io/educated-guess-frontend:v1

cd ..
```

### Step 5.3: Update Kubernetes Manifests

Update the image references in your deployment files:

**Edit:** `infrastructure/aks/deployment/backend-deployment.yaml`
```yaml
# Change line with image to:
image: educatedguessacr.azurecr.io/educated-guess-backend:v1
```

**Edit:** `infrastructure/aks/deployment/frontend-deployment.yaml`
```yaml
# Change line with image to:
image: educatedguessacr.azurecr.io/educated-guess-frontend:v1
```

### Step 5.4: Deploy to AKS

```bash
# Deploy ConfigMaps
kubectl apply -f infrastructure/aks/deployment/configmap.yaml -n educated-guess

# Deploy Backend
kubectl apply -f infrastructure/aks/deployment/backend-deployment.yaml -n educated-guess
kubectl apply -f infrastructure/aks/service/backend-service.yaml -n educated-guess

# Deploy Frontend
kubectl apply -f infrastructure/aks/deployment/frontend-deployment.yaml -n educated-guess
kubectl apply -f infrastructure/aks/service/frontend-service.yaml -n educated-guess

# Check deployment status
kubectl get pods -n educated-guess
kubectl get services -n educated-guess
```

**Expected output:**
```
NAME                                    READY   STATUS    RESTARTS   AGE
backend-deployment-xxx-yyy              1/1     Running   0          2m
frontend-deployment-xxx-zzz             1/1     Running   0          2m
```

### Step 5.5: Get Application URL

```bash
# Wait for external IP to be assigned (may take 2-3 minutes)
kubectl get service frontend-service -n educated-guess --watch

# Once EXTERNAL-IP shows (not <pending>), press Ctrl+C
# Copy the EXTERNAL-IP and visit it in your browser!
```

🎉 Your application should now be accessible at `http://EXTERNAL-IP`

---

## Phase 6: CI/CD Pipeline Setup

### Step 6.1: Push Code to GitHub

```bash
# Initialize git repository (if not already done)
cd c:\Users\Administrator\Downloads\Three_Tier_App
git init

# Add all files
git add .
git commit -m "Initial commit - Educated Guess application"

# Create repository on GitHub (via web interface)
# Then connect your local repo:
git remote add origin https://github.com/YOUR-USERNAME/educated-guess.git
git branch -M main
git push -u origin main
```

### Step 6.2: Create GitHub Secrets

Navigate to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Create the following secrets:

| Secret Name | Value | Where to Find |
|------------|-------|---------------|
| `AZURE_CREDENTIALS` | See Step 6.3 | Azure Service Principal |
| `ACR_USERNAME` | `educatedguessacr` | From Step 4.3 |
| `ACR_PASSWORD` | `<password>` | From Step 4.3 `az acr credential show` |

### Step 6.3: Create Azure Service Principal

```bash
# Get your subscription ID
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Create service principal
az ad sp create-for-rbac \
  --name "educated-guess-github-actions" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/educated-guess-rg \
  --sdk-auth

# Copy the ENTIRE JSON output
# This is your AZURE_CREDENTIALS secret
```

The output looks like:
```json
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx",
  ...
}
```

Paste this entire JSON into the `AZURE_CREDENTIALS` secret in GitHub.

### Step 6.4: Copy GitHub Actions Workflows

```bash
# Create .github/workflows directory in your repo
mkdir -p .github/workflows

# Copy workflow files
cp infrastructure/ci-cd/github-actions-frontend.yaml .github/workflows/
cp infrastructure/ci-cd/github-actions-backend.yaml .github/workflows/

# Commit and push
git add .github/
git commit -m "Add CI/CD pipelines"
git push
```

### Step 6.5: Verify Pipelines

1. Go to your GitHub repository
2. Click **Actions** tab
3. You should see workflows running (may trigger automatically on push)
4. Click on a workflow run to see progress

---

## Phase 7: Verification & Testing

### Step 7.1: Initialize Database

From your local machine:

```bash
# SSH into MongoDB VM
ssh azureuser@$VM_IP

# Copy seed data to VM (from local machine in another terminal)
scp database/seed_data.json azureuser@$VM_IP:~/

# Back in VM SSH session
# Set environment variable for authenticated connection
export MONGODB_URL="mongodb://app_user:YOUR_APP_PASSWORD@localhost:27017/educated_guess?authSource=educated_guess"

# Copy init script to VM (from local machine)
scp database/init_db.py azureuser@$VM_IP:~/

# Install Python dependencies on VM
sudo apt update
sudo apt install python3-pip -y
pip3 install motor

# Run initialization
python3 init_db.py

# Verify data
mongosh -u app_user -p educated_guess --authenticationDatabase educated_guess
use educated_guess
db.content_items.countDocuments()
exit
```

### Step 7.2: Test Application

```bash
# Get your application URL
kubectl get service frontend-service -n educated-guess

# Visit http://EXTERNAL-IP in your browser
```

**Test these features:**
1. ✅ Homepage loads with content grid
2. ✅ Click on category filters
3. ✅ Search functionality works
4. ✅ Individual content items display
5. ✅ Navigation between pages

### Step 7.3: Check Application Logs

```bash
# View backend logs
kubectl logs -l app=backend -n educated-guess --tail=50

# View frontend logs
kubectl logs -l app=frontend -n educated-guess --tail=50

# Check pod status
kubectl get pods -n educated-guess
kubectl describe pod <pod-name> -n educated-guess
```

### Step 7.4: Monitor Resources

```bash
# Check resource usage
kubectl top nodes
kubectl top pods -n educated-guess

# View all resources
kubectl get all -n educated-guess
```

---

## Troubleshooting

### Issue: Pods stuck in "Pending" state

**Diagnosis:**
```bash
kubectl describe pod <pod-name> -n educated-guess
```

**Common causes:**
- Insufficient node resources
- Image pull errors

**Fix:**
```bash
# Scale down if needed
kubectl scale deployment backend-deployment --replicas=1 -n educated-guess

# Or scale up cluster nodes
az aks scale \
  --resource-group educated-guess-rg \
  --name educated-guess-aks \
  --node-count 3
```

### Issue: Cannot connect to MongoDB

**Diagnosis:**
```bash
# Test from a backend pod
kubectl exec -it <backend-pod-name> -n educated-guess -- sh
ping <MONGODB_PRIVATE_IP>
exit
```

**Fix:**
1. Verify NSG rules allow traffic from AKS subnet (10.0.2.0/24)
2. Check MongoDB is running: `ssh azureuser@$VM_IP` then `sudo systemctl status mongod`
3. Verify secret has correct connection string

### Issue: 404 Not Found on frontend

**Fix:**
```bash
# Check if backend service is accessible
kubectl get endpoints -n educated-guess

# Verify environment variables
kubectl exec <frontend-pod-name> -n educated-guess -- env | grep API
```

### Issue: GitHub Actions failing

**Common fixes:**
1. Verify all GitHub secrets are set correctly
2. Check ACR credentials are correct
3. Ensure service principal has correct permissions

### Issue: Out of Azure Credits

**Check usage:**
```bash
az consumption usage list --output table
```

**Cost-saving tips:**
- Use smaller VM sizes during development
- Delete resources when not in use:
```bash
az group delete --name educated-guess-rg --yes
```

---

## Next Steps

### Scaling Your Application

```bash
# Scale backend replicas
kubectl scale deployment backend-deployment --replicas=3 -n educated-guess

# Scale frontend replicas
kubectl scale deployment frontend-deployment --replicas=3 -n educated-guess
```

### Add Custom Domain

1. Purchase domain from domain registrar
2. Create DNS A record pointing to LoadBalancer IP
3. Update frontend service to use domain

### Enable HTTPS

```bash
# Install cert-manager for automatic SSL certificates
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

### Set Up Monitoring

```bash
# Enable Azure Monitor for containers
az aks enable-addons \
  --resource-group educated-guess-rg \
  --name educated-guess-aks \
  --addons monitoring
```

---

## Cleanup (When Done Testing)

> ⚠️ **Warning:** This deletes ALL resources and is irreversible!

```bash
# Delete the entire resource group
az group delete \
  --name educated-guess-rg \
  --yes \
  --no-wait

# This removes:
# - AKS cluster
# - MongoDB VM
# - Container Registry
# - Virtual Network
# - All other resources
```

---

## Support & Resources

- **Azure Documentation**: [docs.microsoft.com/azure](https://docs.microsoft.com/azure)
- **Kubernetes Documentation**: [kubernetes.io/docs](https://kubernetes.io/docs)
- **MongoDB Documentation**: [docs.mongodb.com](https://docs.mongodb.com)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React Documentation**: [react.dev](https://react.dev)

---

## Summary Checklist

Use this to track your progress:

- [ ] Azure account created and CLI installed
- [ ] Resource group created
- [ ] MongoDB VM created and configured
- [ ] MongoDB users created
- [ ] AKS cluster created
- [ ] kubectl configured
- [ ] Container Registry created
- [ ] AKS connected to ACR
- [ ] Kubernetes secrets created
- [ ] Docker images built and pushed
- [ ] Kubernetes deployments created
- [ ] Application accessible via browser
- [ ] GitHub repository created
- [ ] GitHub secrets configured
- [ ] CI/CD pipelines working
- [ ] Database initialized with seed data
- [ ] Application tested and verified

🎉 **Congratulations!** You've successfully deployed a three-tier application to Azure!
