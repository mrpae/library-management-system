#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# Import all required python packages
docker exec -it py bash -c "pip install /scripts/requirements.txt"

# Run initialization SQL scripts
psql -U $POSTGRES_USER -d library-management-system -f /tmp/resources/create_tables.sql
psql -U $POSTGRES_USER -d library-management-system -f /tmp/resources/populate_tables.sql

echo "All initialization scripts completed."