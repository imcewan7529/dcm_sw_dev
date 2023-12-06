import json
import random
import pika
import time

# RabbitMQ setup parameters
RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'DCM_Main_Exchange'
SEND_INTERVAL = 0.1  # 100ms

def generate_test_entry():
    """Generates a single test entry."""
    return {
        "Date/Time": 0,
        "Flow_Rate": round(random.uniform(0, 10), 2)
    }

def send_to_rabbitmq(entry, channel):
    """Sends a given entry to RabbitMQ."""
    message = json.dumps(entry)
    print(message)
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='', body=message)

def main():
    # Setup RabbitMQ connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    try:
        while True:  # Continuous loop
            entry = generate_test_entry()
            send_to_rabbitmq(entry, channel)
            time.sleep(SEND_INTERVAL)  # Wait for 100ms
    except KeyboardInterrupt:
        print("Stopped sending data.")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
