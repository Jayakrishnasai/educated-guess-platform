# 🚀 Quick Deployment Reference

> This is a condensed command reference for experienced users. For detailed explanations, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## Prerequisites

```bash
# Install Azure CLI, kubectl, git
choco install azure-cli kubernetes-cli git -y

# Login to Azure
az login
az account set --subscription "YOUR-SUBSCRIPTION-NAME"
```

## 1. Create Infrastructure (10 minutes)

```bash
# Variables
RG="educated-guess-rg"
LOCATION="eastus"
ACR_NAME="educatedguessacr"
AKS_NAME="educated-guess-aks"
VNET_NAME="educated-guess-vnet"

# Resource Group
az group create --name $RG --location $LOCATION

# Virtual Network
az network vnet create \
  --resource-group $RG \
  --name $VNET_NAME \
  --address-prefix 10.0.0.0/16 \
  --subnet-name database-subnet \
  --subnet-prefix 10.0.1.0/24

az network vnet subnet create \
  --resource-group $RG \
  --vnet-name $VNET_NAME \
  --name aks-subnet \
  --address-prefix 10.0.2.0/24

# MongoDB VM
az network nsg create --resource-group $RG --name mongodb-nsg

az network nsg rule create \
  --resource-group $RG \
  --nsg-name mongodb-nsg \
  --name AllowSSH \
  --priority 1000 \
  --destination-port-ranges 22 \
  --protocol Tcp \
  --access Allow

az network nsg rule create \
  --resource-group $RG \
  --nsg-name mongodb-nsg \
  --name AllowMongoDB \
  --priority 1001 \
  --source-address-prefixes 10.0.2.0/24 \
  --destination-port-ranges 27017 \
  --protocol Tcp \
  --access Allow

az vm create \
  --resource-group $RG \
  --name mongodb-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --vnet-name $VNET_NAME \
  --subnet database-subnet \
  --nsg mongodb-nsg \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Get VM IPs
VM_IP=$(az vm show -d --resource-group $RG --name mongodb-vm --query publicIps -o tsv)
VM_PRIVATE_IP=$(az vm show -d --resource-group $RG --name mongodb-vm --query privateIps -o tsv)
echo "Public IP: $VM_IP"
echo "Private IP: $VM_PRIVATE_IP"

# AKS Cluster (5-10 min)
az aks create \
  --resource-group $RG \
  --name $AKS_NAME \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --vnet-subnet-id /subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/Microsoft.Network/virtualNetworks/$VNET_NAME/subnets/aks-subnet \
  --enable-managed-identity \
  --generate-ssh-keys \
  --network-plugin azure

# Container Registry
az acr create --resource-group $RG --name $ACR_NAME --sku Basic
az acr update --name $ACR_NAME --admin-enabled true
az aks update --resource-group $RG --name $AKS_NAME --attach-acr $ACR_NAME

# Get ACR credentials
az acr credential show --name $ACR_NAME
```

## 2. Setup MongoDB (5 minutes)

```bash
# Copy and run installation script
scp infrastructure/vm/mongodb-install.sh azureuser@$VM_IP:~/
ssh azureuser@$VM_IP "sudo bash mongodb-install.sh"

# Create users
ssh azureuser@$VM_IP << 'EOF'
mongosh << 'MONGO'
use admin
db.createUser({user: "admin", pwd: "CHANGE_THIS_PASSWORD", roles: ["root"]})
exit
MONGO

mongosh -u admin -p << 'MONGO'
use educated_guess
db.createUser({
  user: "app_user",
  pwd: "CHANGE_THIS_APP_PASSWORD",
  roles: [{role: "readWrite", db: "educated_guess"}]
})
exit
MONGO
EOF
```

## 3. Deploy Application (10 minutes)

```bash
# Connect to AKS
az aks get-credentials --resource-group $RG --name $AKS_NAME

# Create secrets
kubectl create namespace educated-guess

kubectl create secret generic mongo-secret \
  --from-literal=mongodb-url="mongodb://app_user:YOUR_PASSWORD@$VM_PRIVATE_IP:27017/educated_guess?authSource=educated_guess" \
  --namespace educated-guess

kubectl create secret generic jwt-secret \
  --from-literal=secret-key="$(openssl rand -base64 32)" \
  --namespace educated-guess

# Build and push images
az acr login --name $ACR_NAME

cd backend
docker build -t $ACR_NAME.azurecr.io/educated-guess-backend:v1 .
docker push $ACR_NAME.azurecr.io/educated-guess-backend:v1
cd ..

cd frontend
docker build -t $ACR_NAME.azurecr.io/educated-guess-frontend:v1 .
docker push $ACR_NAME.azurecr.io/educated-guess-frontend:v1
cd ..

# Deploy to AKS
kubectl apply -f infrastructure/aks/deployment/configmap.yaml -n educated-guess
kubectl apply -f infrastructure/aks/deployment/backend-deployment.yaml -n educated-guess
kubectl apply -f infrastructure/aks/service/backend-service.yaml -n educated-guess
kubectl apply -f infrastructure/aks/deployment/frontend-deployment.yaml -n educated-guess
kubectl apply -f infrastructure/aks/service/frontend-service.yaml -n educated-guess

# Get application URL
kubectl get service frontend-service -n educated-guess --watch
```

## 4. Initialize Database

```bash
# Copy seed data and init script to VM
scp database/seed_data.json database/init_db.py azureuser@$VM_IP:~/

# Run initialization
ssh azureuser@$VM_IP << 'EOF'
sudo apt update && sudo apt install python3-pip -y
pip3 install motor
export MONGODB_URL="mongodb://app_user:YOUR_PASSWORD@localhost:27017/educated_guess?authSource=educated_guess"
python3 init_db.py
EOF
```

## 5. Setup CI/CD

```bash
# Create service principal
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
az ad sp create-for-rbac \
  --name "educated-guess-github-actions" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RG \
  --sdk-auth

# Copy workflows
mkdir -p .github/workflows
cp infrastructure/ci-cd/*.yaml .github/workflows/

# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/educated-guess.git
git push -u origin main
```

**GitHub Secrets Required:**
- `AZURE_CREDENTIALS` - Output from service principal creation
- `ACR_USERNAME` - From `az acr credential show`
- `ACR_PASSWORD` - From `az acr credential show`

## Verification Commands

```bash
# Check pods
kubectl get pods -n educated-guess

# Check services
kubectl get services -n educated-guess

# View logs
kubectl logs -l app=backend -n educated-guess --tail=50
kubectl logs -l app=frontend -n educated-guess --tail=50

# Check resources
kubectl get all -n educated-guess
```

## Cleanup

```bash
# Delete everything
az group delete --name $RG --yes --no-wait
```

## Troubleshooting

```bash
# Pod issues
kubectl describe pod <pod-name> -n educated-guess
kubectl logs <pod-name> -n educated-guess

# Scale deployments
kubectl scale deployment backend-deployment --replicas=1 -n educated-guess

# Test connectivity to MongoDB from pod
kubectl exec -it <backend-pod> -n educated-guess -- sh
ping $VM_PRIVATE_IP
```
