setting up Postgres

```
psql -U postgres -p 5433
CREATE DATABASE service_app;
CREATE USER service_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE service_app TO service_user;

-- Switch to the `service_app` database
\c service_app;

-- Grant usage and creation privileges on the `public` schema
GRANT USAGE ON SCHEMA public TO service_user;
GRANT CREATE ON SCHEMA public TO service_user;

-- Grant all privileges on all tables in the `public` schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO service_user;

-- Grant all privileges on all sequences in the `public` schema
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO service_user;

-- Grant all privileges on all functions in the `public` schema
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO service_user;

service_app=# \dn+ public

service_app=# ALTER SCHEMA public OWNER TO service_user;

service_app=# DROP TABLE IF EXISTS "user" CASCADE;
```