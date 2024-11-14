#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# Run initialization SQL scripts
psql -U $POSTGRES_USER -d library-management-system -f /tmp/scripts/create_books.sql
psql -U $POSTGRES_USER -d library-management-system -f /tmp/scripts/create_borrowers.sql
psql -U $POSTGRES_USER -d library-management-system -f /tmp/scripts/create_adminaccs.sql
psql -U $POSTGRES_USER -d library-management-system -f /tmp/scripts/create_transactions.sql
psql -U $POSTGRES_USER -d library-management-system -f /tmp/scripts/create_historys.sql

echo "All initialization scripts completed."