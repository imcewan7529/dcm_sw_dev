# Library imports
import os
import shutil
import subprocess
import psutil
import glob
import re
import json

MAX_STORAGE_USAGE = 30_000_000_000
STORAGE_FILEPATH = "/tmp/storage_uploads/*.json"
MOUNT_POINT = '/home/pi/usb_mount'
USER='pi'

def cleanup(filepath):
    # Delete file from tmp
    json_files_temp = glob.glob(filepath)
    for file in json_files_temp:
        os.remove(file)

def device_test(device, mount_point, user):
    retry_attempts = 0
    while(retry_attempts < 10):
        test_file = os.path.join(mount_point, 'temp_test_file')
        try:
            # Try creating a temporary file
            with open(test_file, 'w') as file:
                file.write('test')
            # Clean up
            os.remove(test_file)
            return True
        except IOError:
            # Unmount and remount the drive
            try:
                subprocess.run(['sudo', 'umount', '/home/pi/usb_mount'], check=True)
                subprocess.run(['sudo', 'mount', '-o', f'uid={user},gid={user}', device, mount_point], check=True)
                retry_attempts += 1
            except subprocess.CalledProcessError as e:
                print(e)
                return False
    return False
def find_usb_device_path():
    try:
        output = subprocess.check_output(['lsblk', '-J'], text=True)
        devices = json.loads(output)

        for device in devices['blockdevices']:
            # Check if device is removable
            if device.get('rm', False) == True:
                # Adjust the index to 0 to target 'sda1'
                if device['children'] and len(device['children']) > 0:
                    device_path = '/dev/' + device['children'][0]['name']
                    return device_path
        return None
    except subprocess.CalledProcessError as e:
        print("Error executing lsblk:", e)
        return None

def is_usb_connected():
    usb_device_path = '/dev/disk/by-id/'

    # Check if the path exists to prevent errors
    if not os.path.exists(usb_device_path):
        return False

    # Search for USB identifiers
    for device in os.listdir(usb_device_path):
        if 'usb' in device.lower() or 'sd' in device.lower():
            return True
    return False

def is_mounted(path):
    """Check if the path is already mounted."""
    return os.path.ismount(path)

def mount_usb(device, mount_point, user):
    # Create the mount point directory if it doesn't exist
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)

    # Attempt to mount the USB drive
    try:
        subprocess.run(['sudo', 'mount', '-o', f'uid={user},gid={user}', device, mount_point], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error mounting the device: {e}")
        return False

def storage_manager_main():
    # Check that usb is connected
    if not is_usb_connected():
        return False
    
    # If usb is connected and not mounted, attempt to mount it
    if not is_mounted(MOUNT_POINT):
        if not mount_usb(find_usb_device_path(), MOUNT_POINT, USER):
            print("Mount failed")
            return False
        else:
            print("Mount success")
    
    # Test device
    if not device_test(find_usb_device_path(), MOUNT_POINT, USER):
        return False

    json_files_temp = glob.glob(STORAGE_FILEPATH)

    # If no files in /tmp, return false
    if not json_files_temp:
        return False

    for file_path in json_files_temp:
        # If storage is out
        storage_usage = psutil.disk_usage(MOUNT_POINT)
        if storage_usage.used > MAX_STORAGE_USAGE:
            # Delete oldest created file
            json_files_media = glob.glob("/home/pi/usb_mount/*.json")
            # Sort the files with first added at the top
            sorted_json = sorted(json_files_media, key=lambda x: os.path.getctime(x), reverse=False)
            print("Removing:", str(sorted_json[0]))
            os.remove(sorted_json[0])

        shutil.copy(file_path, MOUNT_POINT)
        print("Saved:", str(file_path), "to", str(MOUNT_POINT))
    # Cleanup
    cleanup(STORAGE_FILEPATH)
    return True
