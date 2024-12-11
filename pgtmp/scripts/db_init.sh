#!/bin/bash

set -e

# Wait for PostgreSQL to be ready
until pg_isready -h db -U ${POSTGRES_USER}; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

# Set PGPASSWORD for authentication
export PGPASSWORD=${POSTGRES_PASSWORD}

# Run initialization SQL scripts
psql -h db -U $POSTGRES_USER -d library-management-system -f /tmp/scripts/create_tables.sql
psql -h db -U $POSTGRES_USER -d library-management-system -f /tmp/scripts/populate_tables.sql

echo "All initialization scripts completed."
