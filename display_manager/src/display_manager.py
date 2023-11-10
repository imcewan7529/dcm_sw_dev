# display_manager.py
'''
PIN DEFINITIONS:
DISPLAY ->  RPI_GPIO
VSYS    ->  PIN2 (5V)
GND     ->  PIN6 (GND)
DC      ->  PIN18 (GPIO 24)
CS      ->  PIN12 (SPI1 CE0)
CLK     ->  PIN40 (SCLK1)
DIN     ->  PIN38 (MOSI1)
RST     ->  PIN16 (GPIO 23)
KEY0    ->  PIN31 (GPI0 6)
KEY1    ->  PIN29 (GPIO 5)
'''
# Library imports
from luma.oled.device import sh1107
from luma.core.interface.serial import spi
from time import sleep
import subprocess
import threading
import RPi.GPIO as GPIO
from time import time
from queue import Queue

# Screen imports
import screen_init
import screen_main
import screen_fuel_reset_confirmation
import screen_fuel_reset

# Subtask imports
from service_fuel_level import service_fuel_level_main
from service_status_checker import service_status_checker_main

# === HELPER FUNCTIONS ===
# Quick check for internet connectivity
def is_connected():
    try:
        # Ping google.com to see if there's an internet connection
        subprocess.check_output(['ping', '-c', '1', 'google.com'])
        return True
    except subprocess.CalledProcessError:
        return False

# Purge all messages from a queue
def purge_queue(q):
    while not q.empty():
        try:
            q.get_nowait()
        except Queue.Empty:
            # This exception will be raised if the queue becomes empty 
            # between the time of the .empty() check and the .get_nowait() call.
            # It's okay to silently pass this exception.
            pass


# Display manager class
class DisplayManager:
    def __init__(self, device):
        self.device = device

        # State machine
        self.current_screen = 'INIT'  
        self.previous_screen = 'INIT'
        
        # State machine flags
        self.BOOT_FLAG = True 
        self.buttons_released = False
        self.MAIN_ANIMATION_FLAG = True 

        # State dictionary
        # Default values
        self.state = {
            'fuel_level': 0, 
            'internet_status': is_connected(),
            'module_status': 'LOGGING'
        }
        self.prev_state = self.state.copy()  # To track changes

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        self.button_0 = 5
        self.button_1 = 6
        GPIO.setup(self.button_0, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Assuming buttons connect to GND when pressed
        GPIO.setup(self.button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Kick off connectivity check thread
        self.start_checking_connection()

        # Start the fuel level service thread
        self.fuel_level_service_queue_rx = Queue()
        self.fuel_level_service_queue_tx = Queue()
        self.fuel_level_calc_task = threading.Thread(target = service_fuel_level_main, args=(self.fuel_level_service_queue_rx, self.fuel_level_service_queue_tx))
        self.fuel_level_calc_task.start()

        # Start the status checking thread
        self.service_status_checker_queue_rx = Queue()
        self.service_status_checker_task = threading.Thread(target = service_status_checker_main, args=(self.service_status_checker_queue_rx,))
        self.service_status_checker_task.start()

        # Display init screen on start
        screen_init.display(self.device)

    ## Internet connectivity checks ## 
    def start_checking_connection(self):
        # This will start the internet connection check immediately and then every 30 seconds.
        threading.Timer(30, self.check_connection).start()

    def check_connection(self):
        self.state['internet_status'] = is_connected()
        # Continue checking every 30 seconds
        self.start_checking_connection()

    ## Fuel level calc service hooks ##
    def check_fuel_level(self):
        if not self.fuel_level_service_queue_rx.empty():
            self.state['fuel_level'] = self.fuel_level_service_queue_rx.get()

    ## Status checker hooks ##
    def check_module_status(self):
        if not self.service_status_checker_queue_rx.empty():
            self.state['module_status'] = self.service_status_checker_queue_rx.get()

    ## Main run function ##
    def run(self):
        while True:
            if not(self.current_screen == self.previous_screen) or self.state_changed():
                if self.current_screen == 'INIT':
                    screen_init.display(self.device)
                    self.previous_screen = 'INIT'
                elif self.current_screen == 'MAIN':
                    screen_main.display(self.device, self.state['fuel_level'], self.state['internet_status'], self.state['module_status'], self.MAIN_ANIMATION_FLAG)
                    if self.MAIN_ANIMATION_FLAG:
                        self.MAIN_ANIMATION_FLAG = False
                    self.previous_screen = 'MAIN'
                elif self.current_screen == 'FUEL_RESET_CONFIRM':
                    screen_fuel_reset_confirmation.display(self.device)
                    self.previous_screen = 'FUEL_RESET_CONFIRM'
                elif self.current_screen == 'FUEL_RESET':
                    self.state['fuel_level'] = screen_fuel_reset.display(self.device, self.button_0, self.button_1)
                    self.fuel_level_service_queue_tx.put(self.state['fuel_level'])
                    # Purge whatever accumulated in the queue while user was resetting fuel
                    purge_queue(self.fuel_level_service_queue_rx)
                    self.MAIN_ANIMATION_FLAG = True
                    self.previous_screen == 'FUEL_RESET'
                else:
                    self.current_screen = 'INIT'
                    self.previous_screen = 'FAULT'

            # Update current state
            self.state_update()

    def state_changed(self):
        """Checks if there's been a change in any state parameter."""
        if self.state != self.prev_state:
            self.prev_state = self.state.copy()  # Update the previous state
            return True
        return False

    ## State Machine Updater ##
    def state_update(self):
        if self.BOOT_FLAG:
            sleep(3)
            self.current_screen = 'MAIN'
            self.BOOT_FLAG = False

        # Check both buttons simultaneously pressed for 3 seconds
        elif self.current_screen == 'MAIN':
            if not GPIO.input(self.button_0) and not GPIO.input(self.button_1):  # Both buttons are pressed
                start_time = time()
                while not GPIO.input(self.button_0) and not GPIO.input(self.button_1):  # Continue checking while both buttons remain pressed
                    if time() - start_time >= 3:  # 3 seconds have passed
                        self.current_screen = 'FUEL_RESET_CONFIRM'
                        self.buttons_released = False
                        break
                    sleep(0.1) # prevent 100% cpu usage

        elif self.current_screen == 'FUEL_RESET_CONFIRM':
            # Ensure user has released both buttons before they are used to navigate
            if GPIO.input(self.button_0) and GPIO.input(self.button_1):
                self.buttons_released = True

            if self.buttons_released:
                # Cancel request
                if not GPIO.input(self.button_0):
                    self.current_screen = 'MAIN'
                # Confirm request
                if not GPIO.input(self.button_1):
                    self.current_screen = 'FUEL_RESET'
                # Else wait for input
        
        elif self.current_screen == 'FUEL_RESET':
            self.current_screen = 'MAIN'
        
        # Update every 100ms
        
        # Check the fuel level
        self.check_fuel_level()
        self.check_module_status()
        sleep(0.1)

if __name__ == "__main__":
    serial_interface = spi(port=1, device=0, gpio_DC=24, gpio_RST=23)
    device = sh1107(serial_interface, rotate=3)
    manager = DisplayManager(device)
    manager.run()
