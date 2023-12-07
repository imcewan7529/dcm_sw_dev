# Library imports
import requests
import time
import glob
import os

# Subtask imports
from StorageManager import storage_manager_main
from WiFiUploader import wifi_uploader_main

# Run StorageManager
storage_result = storage_manager_main()

# Check if acknowledgment is received from StorageManager
storage_done = storage_result == "done"

# Check for Wi-Fi connection
while True:
    # Connected:
    try:
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()

        # Run WiFi Uploader
        wifi_result = wifi_uploader_main()

        # Check if acknowledgment is received from WiFiUploader
        wifi_done = wifi_result == "done"
        break

    # Not connected:
    except requests.RequestException:
        time.sleep(5)

if __name__ == "__main__":
    if storage_done and wifi_done:
        # Delete file from tmp
        json_files_temp = glob.glob("/tmp/*.json")
        for file in json_files_temp:

            # Sort the files with last added at the top
            sorted_json = sorted(json_files_temp, key=lambda x: os.path.getctime(x), reverse=True)
            os.remove(sorted_json(0))
    else:
        time.sleep(5)
