from time import sleep

'''
Status Byte Info
Bit 0: ADC Status
Bit 1: Logging Status
'''

import subprocess

def get_service_status(service_name):
    """
    Check the systemd service status for the given service name.
    :param service_name: The name of the systemd service.
    :return: True if the service is active, False otherwise.
    """
    try:
        # Run the 'systemctl is-active' command which returns 'active' if the service is running
        result = subprocess.run(['systemctl', 'is-active', service_name], stdout=subprocess.PIPE, text=True, check=True)
        # Return True if the service is active
        return result.stdout.strip() == 'active'
    except subprocess.CalledProcessError:
        # If the service is not active or the command fails, return False
        return False

def set_bit_status(status_byte, bit_position, service_status):
    """
    Set or clear the specific bit in status_byte based on the service status.
    :param status_byte: The current status byte.
    :param bit_position: The bit position to set or clear (0 for adc_manager, 1 for logging_manager).
    :param service_status: The boolean status of the service.
    :return: The updated status byte.
    """
    if service_status:
        # Clear the bit to 0 if the service is active
        status_byte &= ~(1 << bit_position)
        
    else:
        # Set the bit to 1 if the service is not active (set fault)
        status_byte |= (1 << bit_position)
        
    return status_byte

def set_adc_manager_status(status_byte):
    # Get the service status
    service_status = get_service_status('adc_manager')
    # Set the bit accordingly
    return set_bit_status(status_byte, 0, service_status)

def set_logging_manager_status(status_byte):
    # Get the service status
    service_status = get_service_status('logging_manager')
    # Set the bit accordingly
    return set_bit_status(status_byte, 1, service_status)

def service_status_checker_main(queue_tx):
    status_byte = 0

    while 1:
        # Get ADC Manager Status
        status_byte = set_adc_manager_status(status_byte)
        # Get Logging Status
        status_byte = set_logging_manager_status(status_byte)

        str_status_byte = format(status_byte, '02X')
        if status_byte == 0:
            queue_tx.put("LOGGING")
        else:
            queue_tx.put(str("Err: 0x"  + str_status_byte))
        sleep(60)
