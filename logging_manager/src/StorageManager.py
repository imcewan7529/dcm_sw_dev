import os
import shutil
import psutil
import time

storage_directory = "/media/files"

# Read data from tmp directory
tmp_path = "/tmp"

for files in os.listdir(tmp_path):
    file_path = os.path.join(tmp_path, files)

    if os.path.isfile(file_path) and files.endswith(".json"):
        print(files)
        with open(file_path, 'r') as file:
            read_data = file.read()
            print(read_data)

    else:
        print("File not found")

# Check if device is plugged
# If no device detected, wait 30 seconds then try again
while not os.path.exists(storage_directory):
    print("Storage not connected")
    time.sleep(30)

    # If storage is detected
    print("Storage connected")

    # If there is enough storage
    storage_usage = psutil.disk_usage(storage_directory)
    if storage_usage.used < 30000000000:
        print("There is enough storage")

        # Copy top most file into external storage
        last_created_file, last_created_data = read_data[0]
        shutil.copy(os.path.join(temp_directory_path, last_created_file), storage_directory)

    # Else if storage is out
    else:
        print("Not enough storage")

        # Delete oldest created file
        first_created_file, first_created_data = read_data[-1]
        first_file_path = os.path.join(temp_directory_path, first_created_file)
        os.remove(first_file_path)

        # Go back to while loop
        break

# Else if unplugged
else:
    print("Storage not connected")

done = True
