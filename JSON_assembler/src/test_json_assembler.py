from datetime import datetime
import json
import os
import pika

data_received = {"fuel_level": 100.00}

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
    print("Temporary Directory:", new_file)

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
