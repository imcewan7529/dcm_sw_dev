# Library imports
import time
from datetime import datetime
import json
import os

# ----------- Add back lines 15,16,58 ------------ for final implementation ---------------

WIFI_FILEPATH = '/tmp/wifi_uploads/'
STORAGE_FILEPATH = '/tmp/storage_uploads/'

def json_assembler_main():

    # Creating directories in tmp
    #os.makedirs(STORAGE_FILEPATH)
    #os.makedirs(WIFI_FILEPATH)

    # Needs to be replaced with data from adc_manager
    data_received = {"fuel_level": 100.00}

    try:
        data_json = json.dumps(data_received)
        data_dict = json.loads(data_json)
        print(f"Data as a dictionary: {data_dict}")

    except json.JSONDecodeError as e:
        print("Failed to parse as JSON")
        return False

    else:
        print("Successfully parsed as JSON")

    # Write as a file
    try:
        current_time = datetime.now().strftime("%m_%d_%Y_%H:%M:%S")
        new_file_storage = os.path.join(STORAGE_FILEPATH, f'{current_time}.json')
        new_file_wifi = os.path.join(WIFI_FILEPATH, f'{current_time}.json')
        print("Temporary Directory:", new_file_storage)

        with open(new_file_storage, 'w') as json_file_storage:
            json.dump(data_received, json_file_storage)

        with open(new_file_wifi, 'w') as json_file_wifi:
            json.dump(data_received, json_file_wifi)

    except PermissionError:
        print("Does not have permission to access file")

    except FileNotFoundError:
        print("File not found")

    except Exception as e:
        print(f"Error writing to JSON file: {str(e)}")

    else:
        print("Successfully written JSON file")
        #time.sleep(30)
    return True
