# MongoDB VM Setup Guide

## Overview
This guide explains how to set up a MongoDB VM on Azure for the Educated Guess application.

## Prerequisites
- Azure subscription
- Azure CLI installed
- SSH key pair

## VM Creation

### 1. Create Resource Group
```bash
az group create \
  --name educated-guess-rg \
  --location eastus
```

### 2. Create Virtual Machine
```bash
az vm create \
  --resource-group educated-guess-rg \
  --name mongodb-vm \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --public-ip-sku Standard
```

### 3. Open MongoDB Port (Temporary)
```bash
az vm open-port \
  --resource-group educated-guess-rg \
  --name mongodb-vm \
  --port 27017 \
  --priority 1010
```

## MongoDB Installation

### 1. Connect to VM
```bash
ssh azureuser@<VM_PUBLIC_IP>
```

### 2. Run Installation Script
```bash
sudo bash mongodb-install.sh
```

### 3. Create Database Users
```bash
mongosh

# Switch to admin database
use admin

# Create admin user
db.createUser({
  user: 'admin',
  pwd: 'STRONG_PASSWORD_HERE',
  roles: ['root']
})

# Exit and reconnect with authentication
exit
mongosh -u admin -p

# Create application database and user
use educated_guess

db.createUser({
  user: 'app_user',
  pwd: 'APP_PASSWORD_HERE',
  roles: [{
    role: 'readWrite',
    db: 'educated_guess'
  }]
})
```

## Security Configuration

### 1. Configure Firewall
```bash
sudo bash ufw-rules.sh
```

**Important:** Update the `AKS_SUBNET` variable with your actual AKS subnet CIDR.

### 2. Update Network Security Group
```bash
# Get AKS subnet CIDR
az aks show \
  --resource-group educated-guess-rg \
  --name educated-guess-aks \
  --query "agentPoolProfiles[0].vnetSubnetId" -o tsv

# Update NSG to allow only from AKS
az network nsg rule create \
  --resource-group educated-guess-rg \
  --nsg-name mongodb-vm-nsg \
  --name AllowMongoFromAKS \
  --priority 1000 \
  --source-address-prefixes <AKS_SUBNET> \
  --destination-port-ranges 27017 \
  --access Allow \
  --protocol Tcp
```

## Database Initialization

### 1. Upload Seed Data
```bash
# From your local machine
scp ../database/init_db.py azureuser@<VM_IP>:/home/azureuser/
scp ../database/seed_data.json azureuser@<VM_IP>:/home/azureuser/
```

### 2. Install Python Dependencies and Run
```bash
# On the VM
sudo apt-get install -y python3-pip
pip3 install motor pymongo

# Update MONGODB_URL in init_db.py
python3 init_db.py
```

## Backup Configuration

### 1. Set Up Automated Backups
```bash
# Make backup script executable
chmod +x backup-script.sh

# Update password in backup script
nano backup-script.sh

# Add to crontab (runs daily at 2 AM)
crontab -e
# Add this line:
# 0 2 * * * /home/azureuser/backup-script.sh >> /var/log/mongodb-backup.log 2>&1
```

## Connection String

Update `infrastructure/aks/deployment/mongo-secret.yaml` with:
```
mongodb://app_user:APP_PASSWORD@<VM_PRIVATE_IP>:27017/educated_guess
```

**Use the PRIVATE IP, not public IP, for security!**

## Monitoring

### Check MongoDB Status
```bash
sudo systemctl status mongod
```

### View Logs
```bash
sudo tail -f /var/log/mongodb/mongod.log
```

### Check Connections
```bash
mongosh -u admin -p
use admin
db.currentOp()
db.serverStatus().connections
```

## Maintenance

### Restart MongoDB
```bash
sudo systemctl restart mongod
```

### View Disk Usage
```bash
df -h
du -sh /var/lib/mongodb
```

### Restore from Backup
```bash
cd /var/backups/mongodb
tar -xzf mongodb_backup_YYYYMMDD_HHMMSS.tar.gz
mongorestore \
  --host=localhost \
  --port=27017 \
  --username=admin \
  --password=PASSWORD \
  --authenticationDatabase=admin \
  --db=educated_guess \
  mongodb_backup_YYYYMMDD_HHMMSS/educated_guess
```

## Troubleshooting

### Cannot Connect from AKS
1. Check UFW status: `sudo ufw status`
2. Check MongoDB binding: `grep bindIp /etc/mongod.conf`
3. Check NSG rules in Azure Portal
4. Verify AKS can reach VM: `kubectl run -it --rm debug --image=busybox --restart=Never -- telnet <VM_IP> 27017`

### Performance Issues
1. Check indexes: `db.collection.getIndexes()`
2. Monitor slow queries: `db.setProfilingLevel(1, { slowms: 100 })`
3. Check resource usage: `htop`
