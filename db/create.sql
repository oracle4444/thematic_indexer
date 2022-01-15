CREATE USER indexer_user WITH PASSWORD 'indexer_pass';

CREATE DATABASE indexer_db;
GRANT ALL PRIVILEGES ON DATABASE indexer_db TO indexer_user;