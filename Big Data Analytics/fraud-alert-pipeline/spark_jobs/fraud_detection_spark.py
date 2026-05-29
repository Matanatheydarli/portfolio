from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from kafka import KafkaProducer
import sys
import os
import json


KAFKA_TOPIC = "fraud_alerts"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


def get_partition_for_file(input_file):
    file_name = os.path.basename(input_file)

    if file_name == "part1.csv":
        return 0
    elif file_name == "part2.csv":
        return 1
    else:
        raise ValueError("Input file must be either part1.csv or part2.csv")


def send_frauds_to_kafka(fraud_df, input_file):
    file_name = os.path.basename(input_file)
    partition = get_partition_for_file(input_file)

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )

    fraud_rows = fraud_df.collect()

    print("===================================")
    print(f"Sending fraud alerts from {file_name} to Kafka topic: {KAFKA_TOPIC}")
    print(f"Kafka partition selected: {partition}")
    print("===================================")

    for row in fraud_rows:
        message = row.asDict()
        message["source_file"] = file_name
        message["kafka_topic"] = KAFKA_TOPIC

        producer.send(
            KAFKA_TOPIC,
            value=message,
            partition=partition
        )

        print(f"Sent fraud alert to partition {partition}: {message}")

    producer.flush()
    producer.close()

    print("===================================")
    print(f"Total messages sent to Kafka: {len(fraud_rows)}")
    print("===================================")


def process_file(input_file):
    spark = SparkSession.builder \
        .appName("FraudDetectionProcessing") \
        .master("local[*]") \
        .getOrCreate()

    print("===================================")
    print(f"Starting PySpark job for file: {input_file}")
    print("===================================")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")

    df = spark.read.csv(input_file, header=True, inferSchema=True)

    print("Original data:")
    df.show(5)

    print("Schema:")
    df.printSchema()

    clean_df = df.dropna()

    print("Data after removing missing values:")
    clean_df.show(5)

    fraud_df = clean_df.filter(
        (col("is_first_transaction") == 1) &
        (col("transaction_amount") > 210)
    )

    print("Suspicious transactions found:")
    fraud_df.show(truncate=False)

    fraud_count = fraud_df.count()

    print("===================================")
    print(f"Total suspicious transactions: {fraud_count}")
    print("===================================")

    send_frauds_to_kafka(fraud_df, input_file)

    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python fraud_detection_spark.py <input_csv_file>")

    input_file = sys.argv[1]
    process_file(input_file)
