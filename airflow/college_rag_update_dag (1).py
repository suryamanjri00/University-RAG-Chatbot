# dags/college_rag_update_dag.py

import os
import sys
import yaml
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from scrape_website import scrape_main
from embed_documents import embed_main

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "config.yaml")
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

@dag(
    dag_id="college_rag_update_dag",
    description="Scrape and embed with config params",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="0 2 1 * *",
    catchup=False,
    tags=["college", "rag", "chromadb"],
    params={  # these show up in the UI
        "model_name": config.get("model_name", "mistral"),
        "embedding_model_name": config.get("embedding_model_name", "all-MiniLM-L6-v2"),
        "chunk_size": config.get("chunk_size", 300),
        "batch_size": config.get("batch_size", 2000),
    }
)
def college_rag_update_flow():

    @task()
    def scrape_task():
        print(f"[SCRAPE] Running scrape_main()")
        scrape_main()

    @task()
    def embed_task(params=None):
        print("[EMBED] Running embed_main() with dynamic config (override if needed)")
        # If you want to override config.yaml later, read params here
        # like: params["embedding_model_name"]
        embed_main()

    scrape = scrape_task()
    embed = embed_task()

    scrape >> embed

dag = college_rag_update_flow()
