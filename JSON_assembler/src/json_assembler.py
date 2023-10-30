import pika
import json
from datetime import datetime
import os

# ************************************************************************************
# Global variables
data_received = {"Date/Time": "10/30", "Flow_Rate": 50}

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
queue_name = 'DCM_Main_Exchange'
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
    data_json = json.dumps(data_received)
    data_dict = json.loads(data_json)
    print(f"Data as a dictionary: {data_dict}")

except json.JSONDecodeError as e:
    print("Failed to parse as JSON")

else:
    print("Successfully parsed as JSON")

# Write as a file
try:
    current_time = datetime.now().strftime("%m_%d_%Y_%H:%M:%S")
    new_file = os.path.join('/tmp/', f'{current_time}.json')

    with open(new_file, 'w') as json_file:
        json.dump(data_received, json_file)

except PermissionError:
    print("Does not have permission to access file")

except FileNotFoundError:
    print("File not found")

except Exception as e:
    print(f"Error writing to JSON file: {str(e)}")

else:
    print("Successfully written JSON file")
