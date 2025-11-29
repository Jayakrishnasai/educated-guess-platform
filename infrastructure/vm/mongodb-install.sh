#!/bin/bash

# MongoDB Installation Script for Ubuntu VM
# Run with sudo

set -e

echo "================================"
echo "MongoDB Installation for VM"
echo "================================"

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Import MongoDB public GPG key
echo "Importing MongoDB GPG key..."
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

# Create list file for MongoDB
echo "Adding MongoDB repository..."
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
   tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Reload package database
apt-get update

# Install MongoDB
echo "Installing MongoDB..."
apt-get install -y mongodb-org

# Start MongoDB service
echo "Starting MongoDB service..."
systemctl start mongod
systemctl enable mongod

# Configure MongoDB for remote access
echo "Configuring MongoDB..."
sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongod.conf

# Enable authentication
cat >> /etc/mongod.conf << EOF

# Enable authentication
security:
  authorization: enabled
EOF

# Restart MongoDB
systemctl restart mongod

echo "================================"
echo "MongoDB Installation Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Create admin user:"
echo "   mongosh"
echo "   use admin"
echo "   db.createUser({user: 'admin', pwd: 'YOUR_PASSWORD', roles: ['root']})"
echo ""
echo "2. Create application user:"
echo "   use educated_guess"
echo "   db.createUser({user: 'app_user', pwd: 'YOUR_PASSWORD', roles: [{role: 'readWrite', db: 'educated_guess'}]})"
echo ""
echo "3. Update mongo-secret.yaml with connection string:"
echo "   mongodb://app_user:YOUR_PASSWORD@<VM_IP>:27017/educated_guess"
echo ""
echo "4. Run ufw-rules.sh to configure firewall"
