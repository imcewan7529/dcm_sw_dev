# Library imports
import time
from datetime import datetime
import json
import os
import pika

# ----------- Add back lines 15,16,58 ------------ for final implementation ---------------

WIFI_DIR_PATH = '/tmp/wifi_uploads/'
STORAGE_DIR_PATH = '/tmp/storage_uploads/'

def setup():
    # Check if WIFI_DIR_PATH exists, if not, create it
    if not os.path.exists(WIFI_DIR_PATH):
        os.makedirs(WIFI_DIR_PATH)

    # Check if STORAGE_DIR_PATH exists, if not, create it
    if not os.path.exists(STORAGE_DIR_PATH):
        os.makedirs(STORAGE_DIR_PATH)

def callback(ch, method, properties, body, messages, max_messages):
    # Convert message body from bytes to a dictionary
    message = json.loads(body)
    
    # Append message to the messages dictionary
    messages.append(message)

    # Check if we have reached 300 messages
    if len(messages) >= max_messages:
        ch.stop_consuming()

def listen_for_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'DCM_Main_Exchange'
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    messages = []  # List to store the messages
    max_messages = 10

    # The lambda function allows us to pass extra arguments to callback
    on_message_callback = lambda ch, method, properties, body: callback(ch, method, properties, body, messages, max_messages)
    channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=True)

    channel.start_consuming()

    # Return the messages after consuming is finished
    return messages

def json_assembler_main():
    while True:
        setup()
        messages = listen_for_messages()

        # Get current date and time for the filename
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # File names with date and time
        wifi_file_path = os.path.join(WIFI_DIR_PATH, f"hydrogen_sensor_log_{current_datetime}.json")
        storage_file_path = os.path.join(STORAGE_DIR_PATH, f"hydrogen_sensor_log_{current_datetime}.json")

        # Write messages to files in both directories
        for file_path in [wifi_file_path, storage_file_path]:
            with open(file_path, 'w') as file:
                json.dump(messages, file)
    
