#!/bin/bash
set -e

psql --username "$POSTGRES_USER" -U postgres -c "CREATE USER $DB_USER PASSWORD '$DB_PASS'"
psql --username "$POSTGRES_USER" -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER"

# Testing DB
psql --username "$POSTGRES_USER" -U postgres -c "CREATE USER $DB_USER_TESTING PASSWORD '$DB_PASS_TESTING'"
psql --username "$POSTGRES_USER" -U postgres -c "CREATE DATABASE $DB_NAME_TESTING OWNER $DB_USER_TESTING"
