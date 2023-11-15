from time import sleep
import threading
import pika
import json
from functools import partial
import os
import sys

# Global variables
FLOW_RATE_DATA_POINTS = 0
FLOW_RATE_AVERAGE = 0
FUEL_LEVEL_MAX_LITRES = 100
# Store fuel remaining in a file, stored in liters
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
FUEL_REMAINING_FILENAME = os.path.join(script_directory, 'fuel_remaining.txt')
# File I/O lock
FUEL_REMAINING_FILE_LOCK = threading.Lock()

# Helper functions to deal with file I/O
def get_stored_fuel_remaining():
    global FUEL_REMAINING_FILENAME
    global FUEL_REMAINING_FILE_LOCK
    with FUEL_REMAINING_FILE_LOCK:
        try:
            with open(FUEL_REMAINING_FILENAME, 'r') as file:
                fuel_remaining = file.read()

        except FileNotFoundError:
            with open(FUEL_REMAINING_FILENAME, 'w') as file:
                file.write(str(FUEL_LEVEL_MAX_LITRES))
                fuel_remaining = FUEL_LEVEL_MAX_LITRES

    return float(fuel_remaining)

def update_fuel_remaining_file(fuel_remaining):
    global FUEL_REMAINING_FILENAME
    global FUEL_REMAINING_FILE_LOCK

    with FUEL_REMAINING_FILE_LOCK:
        with open(FUEL_REMAINING_FILENAME, 'w') as file:
            file.write(str(fuel_remaining))


## Fuel level calculation functions ## 
def calculate_fuel_level(flow_rate, queue_tx):
    global FLOW_RATE_DATA_POINTS
    global FLOW_RATE_AVERAGE
    # Increment data points
    FLOW_RATE_DATA_POINTS = FLOW_RATE_DATA_POINTS + 1
    # Update fuel level every 60 seconds
    if (FLOW_RATE_DATA_POINTS < 600):
        FLOW_RATE_AVERAGE = FLOW_RATE_AVERAGE + flow_rate
    else:
        FLOW_RATE_AVERAGE = FLOW_RATE_AVERAGE / FLOW_RATE_DATA_POINTS
        FLOW_RATE_DATA_POINTS = 0
        # Calculate fuel level
        fuel_level_prev = get_stored_fuel_remaining()
        fuel_level = fuel_level_prev - FLOW_RATE_AVERAGE
        FLOW_RATE_AVERAGE = 0
        # Saturate Fuel level
        if (fuel_level < 0):
            fuel_level = 0
        # Update the fuel level file
        update_fuel_remaining_file(fuel_level)
        # Report new fuel level to the display manager
        queue_tx.put(int(round(fuel_level)))

## RabbitMQ helper functions ##
def parse_flow_rate(message_string):
    try:
        # Convert the string into a dictionary
        message_dict = json.loads(message_string)        

        # Extract the flow rate value
        flow_rate = message_dict.get('Flow_Rate', None)

        # Return the flow rate if it exists, otherwise return None
        return float(flow_rate)
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None


def callback(ch, method, properties, body, queue_tx):
    flow_rate = parse_flow_rate(body.decode())
    calculate_fuel_level(flow_rate, queue_tx)

def message_listener(queue_tx):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'DCM_Main_Exchange'
    result = channel.queue_declare(queue='', exclusive=True)
    DCM_Main_Exchange_queue = result.method.queue

    channel.queue_bind(exchange=exchange_name, queue=DCM_Main_Exchange_queue)

    # Here, we're using partial to add the queue_tx argument to the callback
    on_message_callback_with_queue = partial(callback, queue_tx=queue_tx)
    channel.basic_consume(queue=DCM_Main_Exchange_queue, on_message_callback=on_message_callback_with_queue, auto_ack=True)

    channel.start_consuming()

def service_fuel_level_main(queue_tx, queue_rx):
    # Start the message listener
    queue_tx.put(int(round(get_stored_fuel_remaining())))
    message_listener(queue_tx)
    while 1:
        sleep(1) # sleep for 1s
        # If fuel level reset was requested
        if not queue_rx.empty():
            fuel_level = queue_rx.get()
            update_fuel_remaining_file(fuel_level)
            