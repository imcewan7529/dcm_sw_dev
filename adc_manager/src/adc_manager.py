from MCP3008 import MCP3008
from datetime import datetime
from lowpass_filter import Lowpass_Filter
import json  
import time
import random 

# adc driver
adc = MCP3008()

# log file  (will be deleted later) 
filename = '../test_logs/log_test.json'              
log_file = open(filename, 'r+') 
file_data = json.load(log_file)


# writes data to json file (will be moved to Json generator later)
def write_json(new_data, write_file):
    file_data["Voltage_Log"].append(new_data)
    write_file.seek(0)
    json.dump(file_data, write_file, indent=4,sort_keys=True, default=str)


def main():
    p1 = Lowpass_Filter()
    
    while(True):
        value = adc.read(channel = 0)/1023.0 * 5
    
        now = datetime.now()
        #filtered_value = p1.Lowpass_Filter(value)
        #Formats data to json
        fields = {"Date/Time": now, "Voltage": value}
        #write_json(fields, log_file) 
        print("Date: %s | Voltage: %.4f"%  (now , value) )
        # Delaysample
        time.sleep(.1)        

    log_file.close()


if __name__ == "__main__":
    main()

