.PHONY: up down logs psql-source psql-dest ingest minio

up:
    docker compose up -d --build

down:
    docker compose down

logs:
    docker compose logs -f

ingest:
    docker run --rm --network etl-project_elt_network -v "$(CURDIR)/scripts:/scripts" -w /scripts python:3.11-slim bash -c "pip install --quiet boto3 sqlalchemy psycopg2-binary pandas >/dev/null 2>&1 && python ingest_to_s3.py"

psql-source:
    docker exec -it etl-project-source_postgres-1 psql -U postgres -d source_db

psql-dest:
    docker exec -it etl-project-destination_postgres-1 psql -U postgres -d destination_db

minio:
    @echo "MinIO Console: http://localhost:9101  (minioadmin / minioadmin)"