#!/bin/bash

# UFW Firewall Configuration for MongoDB VM
# Run with sudo

set -e

echo "================================"
echo "Configuring UFW Firewall"
echo "================================"

# Enable UFW
echo "Enabling UFW..."
ufw --force enable

# Allow SSH (important!)
echo "Allowing SSH..."
ufw allow 22/tcp

# Allow MongoDB from AKS subnet
# Replace <AKS_SUBNET> with your actual AKS subnet CIDR
AKS_SUBNET="10.240.0.0/16"  # Example - Update this!

echo "Allowing MongoDB from AKS subnet: $AKS_SUBNET..."
ufw allow from $AKS_SUBNET to any port 27017 proto tcp

# Deny MongoDB from all other sources
echo "Denying MongoDB from other sources..."
ufw deny 27017/tcp

# Show status
echo ""
echo "================================"
echo "Firewall Rules:"
echo "================================"
ufw status verbose

echo ""
echo "⚠️  IMPORTANT: Update AKS_SUBNET variable with your actual AKS subnet CIDR"
echo "   You can find this in Azure Portal -> AKS -> Networking"
