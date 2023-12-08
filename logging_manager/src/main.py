# Library imports
import time
import glob
import os

# Subtask imports
from JsonAssembler import json_assembler_main
from StorageManager import storage_manager_main
from WiFiUploader import wifi_uploader_main 

WIFI_FILEPATH = "/tmp/wifi_uploads/*.json"
STORAGE_FILEPATH = "/tmp/storage_uploads/*.json"

def cleanup(filepath):
    # Delete file from tmp
    json_files_temp = glob.glob(filepath)
    for file in json_files_temp:
        os.remove(file)

def main():
    while True:
        if json_assembler_main():
            print("Starting storage_manager")       # For testing only
            if storage_manager_main():
                cleanup(STORAGE_FILEPATH)

            print("Starting wifi_uploader")       # For testing only
            if wifi_uploader_main():
                cleanup(WIFI_FILEPATH)

            # Wait 30 seconds
            time.sleep(30)

if __name__ == "__main__":
    main()

    
