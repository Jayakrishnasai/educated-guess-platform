#!/bin/bash

# MongoDB Backup Script
# Add to crontab for automated backups: 0 2 * * * /path/to/backup-script.sh

set -e

# Configuration
BACKUP_DIR="/var/backups/mongodb"
MONGO_HOST="localhost"
MONGO_PORT="27017"
MONGO_USER="admin"
MONGO_PASSWORD="YOUR_PASSWORD"  # Update this!
DB_NAME="educated_guess"
RETENTION_DAYS=7

# Create backup directory
mkdir -p $BACKUP_DIR

# Generate backup filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="mongodb_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

echo "================================"
echo "MongoDB Backup Script"
echo "================================"
echo "Backup started at: $(date)"
echo "Backup path: $BACKUP_PATH"

# Perform backup
mongodump \
  --host=$MONGO_HOST \
  --port=$MONGO_PORT \
  --username=$MONGO_USER \
  --password=$MONGO_PASSWORD \
  --authenticationDatabase=admin \
  --db=$DB_NAME \
  --out=$BACKUP_PATH

# Compress backup
echo "Compressing backup..."
tar -czf "${BACKUP_PATH}.tar.gz" -C $BACKUP_DIR $BACKUP_NAME
rm -rf $BACKUP_PATH

# Calculate backup size
BACKUP_SIZE=$(du -h "${BACKUP_PATH}.tar.gz" | cut -f1)
echo "Backup size: $BACKUP_SIZE"

# Remove old backups
echo "Removing backups older than $RETENTION_DAYS days..."
find $BACKUP_DIR -name "mongodb_backup_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete

echo "Backup completed at: $(date)"
echo "================================"

# Optional: Upload to Azure Blob Storage
# Uncomment and configure if you want cloud backup
# az storage blob upload \
#   --account-name <STORAGE_ACCOUNT> \
#   --container-name mongodb-backups \
#   --name "${BACKUP_NAME}.tar.gz" \
#   --file "${BACKUP_PATH}.tar.gz"
