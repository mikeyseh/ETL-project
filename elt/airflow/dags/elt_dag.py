import os
from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

HOST_PROJECT_PATH = os.environ.get("HOST_PROJECT_PATH", "/opt/airflow")
DBT_PROJECT_PATH = os.path.join(HOST_PROJECT_PATH, "dbt")
DBT_PROFILES_PATH = os.path.join(HOST_PROJECT_PATH, "dbt", "profiles")

default_args = {"owner": "airflow", "depends_on_past": False}

with DAG(
    dag_id="elt_and_dbt",
    start_date=datetime(2023, 10, 28),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
) as dag:

    dbt_run = DockerOperator(
        task_id="dbt_run",
        image="ghcr.io/dbt-labs/dbt-postgres:1.4.7",
        command="run --profiles-dir /home/airflow/.dbt --project-dir /dbt",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=[
            Mount(source=DBT_PROJECT_PATH, target="/dbt", type="bind"),
            Mount(source=DBT_PROFILES_PATH, target="/home/airflow/.dbt", type="bind"),
        ],
        mount_tmp_dir=False,
    )