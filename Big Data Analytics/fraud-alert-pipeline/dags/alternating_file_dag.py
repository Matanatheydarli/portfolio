from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
import os


DATA_DIR = "/opt/airflow/data"

PART1_FILE = os.path.join(DATA_DIR, "part1.csv")
PART2_FILE = os.path.join(DATA_DIR, "part2.csv")


def choose_and_process_file():
    current_file = Variable.get("next_file_to_process", default_var="part1.csv")

    if current_file == "part1.csv":
        file_path = PART1_FILE
        next_file = "part2.csv"
    else:
        file_path = PART2_FILE
        next_file = "part1.csv"

    print("===================================")
    print(f"Processing file: {current_file}")
    print(f"Full path: {file_path}")
    print("===================================")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        first_line = file.readline()
        print(f"First line of {current_file}: {first_line}")

    Variable.set("next_file_to_process", next_file)

    print(f"Next execution will process: {next_file}")


with DAG(
    dag_id="alternating_csv_processing_dag",
    description="Runs every 10 minutes and alternates between part1.csv and part2.csv",
    start_date=datetime(2025, 1, 1),
    schedule_interval="*/10 * * * *",
    catchup=False,
    tags=["final_project", "airflow", "task1"],
) as dag:

    process_one_file = PythonOperator(
        task_id="process_alternating_file",
        python_callable=choose_and_process_file,
    )
