from kafka import KafkaConsumer, TopicPartition
import requests
import json


# Telegram settings
# Replace these with your own values locally.
# Do not push real token to GitHub.
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "YOUR_CHANNEL_ID"


# Kafka settings
KAFKA_TOPIC = "fraud_alerts"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


def send_telegram_message(message_text):
    """
    Sends alert message to Telegram channel.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": message_text
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Telegram alert sent successfully.")
    else:
        print("Failed to send Telegram alert.")
        print("Status code:", response.status_code)
        print("Response:", response.text)


def main():
    """
    Kafka consumer that listens to fraud_alerts topic
    and sends each fraud alert to Telegram.
    """

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    partitions = [
        TopicPartition(KAFKA_TOPIC, 0),
        TopicPartition(KAFKA_TOPIC, 1)
    ]

    consumer.assign(partitions)

    # For testing old messages, read from beginning.
    # For real-time only, change this to: consumer.seek_to_end(*partitions)
    consumer.seek_to_beginning(*partitions)

    print("Kafka consumer started...")
    print(f"Listening to topic: {KAFKA_TOPIC}")
    print("Waiting for fraud alerts...")

    for message in consumer:
        kafka_message = message.value

        alert_text = f"""
Kafka Alert

Student Name and ID: Matanat Heydarli - 000018080
Topic: {message.topic}
Partition: {message.partition}
Offset: {message.offset}
Status: Fraud Found

Message:
{kafka_message}
"""

        print("Fraud message received from Kafka:")
        print(alert_text)

        send_telegram_message(alert_text)


if __name__ == "__main__":
    main()
