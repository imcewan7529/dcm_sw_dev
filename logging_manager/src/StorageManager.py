# Library imports
import os
import shutil
import psutil
import glob

MAX_STORAGE_USAGE = 30_000_000_000
STORAGE_FILEPATH = "/tmp/storage_uploads/*.json"

def storage_manager_main():
    storage_directory = "/media"

    # If nothings plugged in, return false
    if not os.path.exists(storage_directory):
        return False

    json_files_temp = glob.glob(STORAGE_FILEPATH)

    # If no files in /tmp, return false
    if not json_files_temp:
        return False

    for file_path in json_files_temp:
        # If storage is out
        storage_usage = psutil.disk_usage(storage_directory)
        if storage_usage.used > MAX_STORAGE_USAGE:
            # Delete oldest created file
            json_files_media = glob.glob("/media/*.json")
            # Sort the files with first added at the top
            sorted_json = sorted(json_files_media, key=lambda x: os.path.getctime(x), reverse=False)
            os.remove(sorted_json[0])

        shutil.copy(file_path, storage_directory)

    return True
