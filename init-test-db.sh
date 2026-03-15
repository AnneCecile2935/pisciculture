#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    CREATE DATABASE pisciculture_test;
    GRANT ALL PRIVILEGES ON DATABASE pisciculture_test TO test_user;
EOSQL
