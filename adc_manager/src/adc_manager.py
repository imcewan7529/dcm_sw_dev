from MCP3008 import MCP3008
from datetime import datetime, timezone
from lowpass_filter import Lowpass_Filter

import json
import pika
import time

# adc driver
adc = MCP3008()

# log file  (will be deleted later) 
#filename = '../test_logs/log1hz_RC_Digital.json'              
#log_file = open(filename, 'r+') 
#file_data = json.load(log_file)

# writes data to json file (will be moved to Json generator later)
def write_json(new_data, write_file):
    file_data["Voltage_Log"].append(new_data)
    write_file.seek(0)
    json.dump(file_data, write_file, indent=4,sort_keys=True, default=str)

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

def main():
    p1 = Lowpass_Filter()
    t0 = time.time()
    
    while(True):
        value = adc.read(channel = 0)/1023.0 * 5
    
        now = datetime.now(timezone.utc)
        filtered_value = p1.Lowpass_Filter(value)
        flow_rate = 2*filtered_value

        # Formats data to JSON
        fields = {
            "vehicleID": "HARDWARE_TEMO_DEMO_TEST",
            "flowrate": flow_rate,
            "time": now.isoformat(),
            "hydrogenFuel": True
        }
        json_data = json.dumps(fields)

        # Publish JSON data
        channel.basic_publish(exchange=queue_name,
                            routing_key='',
                            body=json_data)
        print("Date: %s | Voltage: %.4f"%  (now , filtered_value) )
        # Delaysample
        time.sleep(-(time.time() - t0)% .1)        

    connection.close()
    #log_file.close()


if __name__ == "__main__":
    main()

