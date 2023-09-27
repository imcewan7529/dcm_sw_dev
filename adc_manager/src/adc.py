from MCP3008 import MCP3008
from datetime import datetime
import json  
import time


adc = MCP3008()
filename = 'log_test.json'              # Name of log fie
log_file = open(filename, 'r+') 
file_data = json.load(log_file)


# writes data to json file
def write_json(new_data, write_file):
    file_data["Voltage_Log"].append(new_data)
    write_file.seek(0)
    json.dump(file_data, write_file, indent=4,sort_keys=True, default=str)


while(True):

    value = adc.read(channel = 0)
    now = datetime.now()

    #Formats data to json
    fields = {"Date/Time": now, "Voltage": value/1023.0 * 3.3}
    write_json(fields, log_file) 
    print("Date: %s | Voltage: %.4f"% ( now ,(value/1023.0 * 3.3)))

    # Delaysample
    time.sleep(1)

log_file.close()


