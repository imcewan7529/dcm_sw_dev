import requests
import time
import glob
import os

# Call StorageManager
exec(open("StorageManager.py").read())

# Check if acknowledgment is received from StorageManager
if "done" in globals():
    storage_done = True

# Check for Wi-Fi connection
while True:
    # Connected:
    try:
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()

        # Call WiFiUploader
        exec(open("WiFiUploader.py").read())

        # Check if acknowledgment is received from WiFiUploader
        if "done" in globals():
            wifi_done = True

        break

    # Not connected:
    except requests.RequestException:
        time.sleep(5)

# Check if acknowledgment is received from both
if storage_done and wifi_done:
    # Delete file from tmp
    json_files_temp = glob.glob("/tmp/*.json")
    for file in json_files_temp:

        # Sort the files with last added at the top
        sorted_json = sorted(json_files_temp, key=lambda x: os.path.getctime(x), reverse=True)

        os.remove(sorted_json(0))

else:
    time.sleep(5)
