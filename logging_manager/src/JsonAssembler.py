# Library imports
import time
from datetime import datetime
import json
import os

def json_assembler_main():

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
        new_file_storage = os.path.join('/tmp/storage_uploads/', f'{current_time}.json')
        new_file_wifi = os.path.join('/tmp/wifi_uploads/', f'{current_time}.json')
        print("Temporary Directory:", new_file_storage)

        with open(new_file_storage, 'w') as json_file:
            json.dump(data_received, json_file)

        with open(new_file_wifi, 'w') as json_file:
            json.dump(data_received, json_file)
            time.sleep(30)

    except PermissionError:
        print("Does not have permission to access file")

    except FileNotFoundError:
        print("File not found")

    except Exception as e:
        print(f"Error writing to JSON file: {str(e)}")

    else:
        print("Successfully written JSON file")

    return True
