# Phase 1 — Airbyte (Postgres → S3/MinIO)

Original ingestion platform. Infrastructure **restored and running** (10+ containers, UI on :8000, API responds, workspace intact).

## Fixes applied

1. lags.yml was an empty directory → converted to file
2. 	emporal/dynamicconfig/development.yaml was missing → added
3. .env required vars recovered from running containers

## Known limitation

Airbyte 0.44.3 has a cached connector-catalog bug: the worker queries Docker Hub's registry manifest and fails with 'Could not find image' even when the image exists locally, if the digest differs from the worker's boot-time snapshot. Cannot be fixed without upgrading to Airbyte 0.63+ or abctl.

**Workaround:** use scripts/ingest_to_s3.py (Python implementation of the same Postgres → S3 pattern — works today).

## Bring it up
```ncd airbyte
cp .env.example .env
# fill CHANGE_ME values
docker compose up -d
```

Services: UI on :8000 (airbyte/password), Postgres :5455, MinIO :9000/9090.

## Stack

- Airbyte 0.44.3 (server, worker, webapp, temporal, cron, proxy, connector-builder)
- PostgreSQL 15 (DWH :5455)
- MinIO (S3-compatible :9000/9090)
