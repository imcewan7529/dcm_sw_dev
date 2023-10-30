import pika
import json
import time
import datetime
import os

# ************************************************************************************
# Global variables
data_received = None

# Read data from queue
# Callback function
def callback(ch, method, properties, body):
    global data_received
    data_received = body.decode('utf-8')
    print(f"Message received: {data_received}")

# Create connection to MQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Create a channel
channel = connection.channel()

# Connect to queue
queue_name = 'ADCname'
channel.queue_declare(queue=queue_name)

# Consume from queue
channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

try:
    print("Started consuming messages")
    channel.start_consuming()

except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close()

# ************************************************************************************
# Put data into python dictionary
try:
    data_dict = json.loads(data_received)
    print(f"Data as a dictionary: {data_dict}")

except json.JSONDecodeError as e:
    print("Failed to parse as JSON")

else:
    print("Successfully parsed as JSON")

# Write as a file
try:
    while True:
        current_time = datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
        new_file = os.path.join('/tmp/', f'{current_time}.json')

        with open(new_file, 'w') as json_file:
            json.dump(data_dict, json_file)

except FileNotFoundError:
    print("File not found")

except PermissionError:
    print("Does not have permission to access file")

except Exception as e:
    print("Error writing to JSON file")

time.sleep(30)
