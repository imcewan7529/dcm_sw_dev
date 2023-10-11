import pika
import json

# ************************************************************************************
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

# Connect to queue (name is placeholder for given name by ADC)
queue_name = 'ADCname'
channel.queue_declare(queue=queue_name)

# Consume from queue
channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

print("Started consuming messages")

channel.start_consuming()
# ************************************************************************************
# Convert data to json


# Put data into python dictionary
data_dict = json.loads(data_received_str)

# Format as JSON
data_json = json.dumps(data_dict, indent=4)

# Write as a file
with open('data_out.json', 'w') as json_file:
    json_file.write(data_json)
