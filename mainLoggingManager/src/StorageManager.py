import os
import shutil
import psutil
import time

# ******* Functions ***********
# Read data from temp directory
def read_from_temp(temp_dir):
    data_list = []
    temp_files = os.listdir(temp_dir)
    temp_files.sort(key=lambda x: os.path.getctime(os.path.join(temp_dir, x)), reverse=True)

    for files in temp_files:
        files_path = os.path.join(temp_dir, files)
        with open(files_path, 'r') as file:
            data = file.read()
            data_list.append((files, data))

    return data_list
# ****************************

temp_directory_path = "/tmp"
storage_directory = "/media/files"
read_data = read_from_temp(temp_directory_path)

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
