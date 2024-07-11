#!/bin/bash
DATE=$(date +%Y-%m-%d_%H-%M-%S)
pg_dump -U josephine inventory_db > ./backups/backup_$DATE.sql
