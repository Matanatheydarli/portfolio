# Near-Real-Time Fraud Alert Pipeline

This project is an end-to-end near-real-time fraud alert pipeline built with Apache Airflow, PySpark, Apache Kafka, Kafka UI, Docker Compose, and Telegram Bot.

## Project Overview

The pipeline processes transaction CSV files, detects suspicious transactions using PySpark, streams fraud alerts through Kafka, and sends alert messages to Telegram.

## Architecture

Airflow Scheduler → PySpark Processing Job → Kafka Topic `fraud_alerts` → Kafka Consumer → Telegram Bot Alert

## Tools Used

- Apache Airflow
- Apache Spark / PySpark
- Apache Kafka
- Kafka UI
- Docker Compose
- Telegram Bot API
- Python

## Main Features

- Airflow DAG runs every 10 minutes
- Alternates between `part1.csv` and `part2.csv`
- PySpark removes missing values using `dropna()`
- Fraud detection rule: `is_first_transaction == 1` and `transaction_amount > 210`
- Kafka topic `fraud_alerts` uses 2 partitions
- `part1.csv` alerts go to partition 0
- `part2.csv` alerts go to partition 1
- Kafka consumer sends alerts to Telegram

## Project Structure

```text
fraud-alert-pipeline/
├── airflow-docker-compose.yaml
├── dags/
├── data/
├── spark_jobs/
├── consumer/
├── kafka/
├── README.md
└── .gitignore
