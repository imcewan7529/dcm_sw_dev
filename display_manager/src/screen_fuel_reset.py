from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from RPi import GPIO as GPIO
from time import time
from time import sleep
from service_fuel_level import update_fuel_remaining_file

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=10)  # Adjust size as needed
font_fuel_disp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=12)  # Adjust size as needed

FUEL_LEVEL_INC = 100

def display(device, button_0, button_1):
    # Start the new fuel level at 7000L always
    new_fuel_level_L = 7000
    # Flag to ensure user has released button upon entering this state
    button_released = False
    while True:
        content = Image.new("1", device.size, "black")
        draw = ImageDraw.Draw(content)
        draw.text((0,0), "Set Fuel Level:", font=font, fill=255)
        draw.text((0,12), str(new_fuel_level_L) + " L", font=font_fuel_disp, fill=255)
        draw.text((0,26), "Press and hold both\nbuttons for 3s when done.", font=font, fill=255)
        draw.text((105,0), "+ ->", font=font, fill=255)
        draw.text((110,50), "- ->", font=font, fill=255)
        device.display(content)
        
        # GPIO Logic
        # Entry button released
        if GPIO.input(button_1):
            button_released = True
        
        if button_released:
            # Exit logic
            if not GPIO.input(button_0) and not GPIO.input(button_1):  # Both buttons are pressed
                        start_time = time()
                        while not GPIO.input(button_0) and not GPIO.input(button_1):  # Continue checking while both buttons remain pressed
                            if time() - start_time >= 3:  # 3 seconds have passed
                                return new_fuel_level_L
                            sleep(0.1) # prevent 100% cpu

            # Button logic
            elif not GPIO.input(button_0):
                sleep(0.1) # debounce
                new_fuel_level_L = new_fuel_level_L - FUEL_LEVEL_INC
            
            elif not GPIO.input(button_1):
                sleep(0.1) # debounce
                new_fuel_level_L = new_fuel_level_L + FUEL_LEVEL_INC

            # Saturate updated fuel level to value between 7000 - 0
            if new_fuel_level_L > 7000:
                new_fuel_level_L = 7000
            if new_fuel_level_L < 0:
                new_fuel_level_L = 0

            update_fuel_remaining_file(new_fuel_level_L)

        # Small sleep to avoid 100% CPU usage
        sleep(0.1)
        