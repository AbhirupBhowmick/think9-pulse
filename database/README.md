# Database Configuration & Schema (Think9 Pulse)

This directory contains database setup scripts and instructions for Think9 Pulse.

## Prerequisites
- PostgreSQL 15 or higher
- `pgvector` extension installed (`ankane/pgvector`)

## Quick Setup via PostgreSQL CLI

```bash
# Create database
createdb think9_pulse

# Execute initialization script
psql -d think9_pulse -f database/init.sql
```

## Running via Docker

You can launch a pre-configured PostgreSQL instance with pgvector using Docker:

```bash
docker run -d \
  --name think9-postgres \
  -e POSTGRES_DB=think9_pulse \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

Then initialize the schema:

```bash
psql -h localhost -U postgres -d think9_pulse -f database/init.sql
```
