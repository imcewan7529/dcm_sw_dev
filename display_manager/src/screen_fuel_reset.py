from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from RPi import GPIO as GPIO
from time import time
from time import sleep

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=10)  # Adjust size as needed
font_fuel_disp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=12)  # Adjust size as needed


def display(device, button_0, button_1):
    # Start the new fuel level at 100 always
    new_fuel_level = 100
    # Flag to ensure user has released button upon entering this state
    button_released = False
    while True:
        content = Image.new("1", device.size, "black")
        draw = ImageDraw.Draw(content)
        draw.text((0,0), "Set Fuel Level:", font=font, fill=255)
        draw.text((0,12), str(new_fuel_level) + "%", font=font_fuel_disp, fill=255)
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
                                return new_fuel_level
                            sleep(0.1) # prevent 100% cpu

            # Button logic
            elif not GPIO.input(button_0):
                sleep(0.1)
                new_fuel_level = new_fuel_level - 1
            
            elif not GPIO.input(button_1):
                sleep(0.1)
                new_fuel_level = new_fuel_level + 1

            # Saturate updated fuel level to values between 0-100
            if new_fuel_level > 100:
                new_fuel_level = 100
            if new_fuel_level < 0:
                new_fuel_level = 0

        # Small sleep to avoid 100% CPU usage
        sleep(0.1)


        
        