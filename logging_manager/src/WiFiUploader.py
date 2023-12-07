# Library imports
import glob
import json
import os
import requests

def wifi_uploader_main():
    # Get all files from /tmp ending with .json
    json_files_temp = glob.glob("/tmp/*.json")
    for file in json_files_temp:
        print(file)
    print("\n")

    # Sort the files with last added at the top
    sorted_json = sorted(json_files_temp, key=lambda x: os.path.getctime(x), reverse=True)
    print("Sorted JSON files:")
    for file in sorted_json:
        print(file)

    # Grab last added file
    latest_json = sorted_json[0]
    print(f"\n{latest_json}")

    with open(latest_json, "r")as file:
        payload = json.load(file)

    print(f"Data from latest json: {payload}")

    # Making HTTP POST request
    web_url = "https://hnoi.netlify.app/"

    try:
        send_data = requests.post(web_url, data=payload)
        print(send_data.statusCode)

    # Handling errors
    except requests.exceptions.ConnectionError as conerr:
        print(f"Error connecting: {conerr}")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")

    except requests.exceptions.Timeout as timeerr:
        print(f"Timeout Error: {timeerr}")

    except requests.exceptions.RequestException as reqerr:
        print(f"Request error: {reqerr}")

    return "done"
