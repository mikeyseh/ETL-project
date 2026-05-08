from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
}

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
            Mount(
                source=r"C:\Users\proga\Documents\elt\Custom_postgres",  # Host path on Windows
                target="/dbt",                                           # Inside dbt container
                type="bind"
            ),
            Mount(
                source=r"C:\Users\proga\.dbt",                           # Host path to your dbt profiles
                target="/home/airflow/.dbt",
                type="bind"
            )
        ],
        mount_tmp_dir=False,
    )
