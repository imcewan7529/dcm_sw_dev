# Library imports
import glob
import json
import requests
import os

WIFI_FILEPATH = "/tmp/wifi_uploads/*.json"
UPLOAD_URL = "https://hnoi-api.onrender.com/api/vehicleData/uploadManyData"

def cleanup(filepath):
    # Delete file from tmp
    json_files_temp = glob.glob(filepath)
    for file in json_files_temp:
        os.remove(file)

def wifi_uploader_main():
    # Get JSON files to be uploaded
    json_files_temp = glob.glob(WIFI_FILEPATH)

    # If no files in /tmp, return false
    if not json_files_temp:
        return False
    
    # If not connected to internet, return false
    if not requests.get("http://www.google.com", timeout=5):
        return False
    else:
        print("Connected")
    
    # Get all files from /tmp/wifi_uploads ending with .json
    json_files_temp = glob.glob(WIFI_FILEPATH)
    for file_path in json_files_temp:
        try: 
            with open(file_path, "r")as file:
                payload = json.load(file)
        except FileNotFoundError:
            print("File not found")
            continue

        # print(f"Data from latest json: {payload}")

        try:
            send_data = requests.post(UPLOAD_URL, json=payload, timeout=15)
            if send_data.status_code == 200:
                print("Upload Success")
            else:
                print("Upload failed with status code:", str(send_data.status_code))

        # Handling errors
        except requests.exceptions.ConnectionError as conerr:
            (f"Error connecting: {conerr}")

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error: {err}")

        except requests.exceptions.Timeout as timeerr:
            print(f"Timeout Error: {timeerr}")

        except requests.exceptions.RequestException as reqerr:
            print(f"Request error: {reqerr}")

    cleanup(WIFI_FILEPATH)
    return True