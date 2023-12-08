# Library imports
import time
import glob
import os
import threading

# Subtask imports
from JsonAssembler import json_assembler_main
from StorageManager import storage_manager_main
from WiFiUploader import wifi_uploader_main 

WIFI_FILEPATH = "/tmp/wifi_uploads/*.json"
STORAGE_FILEPATH = "/tmp/storage_uploads/*.json"

def run_periodically(function, args=()):
    while True:
        thread = threading.Thread(target=function, args=args)
        thread.start()
        thread.join()
        time.sleep(30)

def main():
    # Create and start the thread for json_assembler_main
    json_thread = threading.Thread(target=json_assembler_main)
    json_thread.start()

    # Starting storage_manager_main every 30 seconds
    storage_thread = threading.Thread(target=run_periodically, args=(storage_manager_main,))
    storage_thread.start()

    # Starting wifi_uploader_main every 30 seconds
    wifi_thread = threading.Thread(target=run_periodically, args=(wifi_uploader_main,))
    wifi_thread.start()

    while True:
        # Sleep the main thread as it doesnt need to do anything else
        time.sleep(1)

if __name__ == "__main__":
    main()

    
