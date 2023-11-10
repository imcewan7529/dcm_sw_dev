# screen_main.py
from luma.core.render import canvas
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from time import sleep

DEFAULT_FUEL_LEVEL = 7000


# Main display function
def display(device, fuel_level, internet_status, module_status, boot_flag): 
    # Get fuel level in terms of percent
    fuel_level = round((fuel_level/DEFAULT_FUEL_LEVEL)* 100) 
    # Set max brightness
    device.contrast(255)

    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=25)  # Adjust size as needed
    font_subtext = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=10)
    font_main_status = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=10)

    # Define the position where you want to draw the symbols
    wifi_x = 6  # adjust as needed
    wifi_y = 60  # adjust as needed

    # Define some parameters for the WiFi symbol
    radius_increment = 5  # adjust as needed
    num_arcs = 3  # number of arcs in the WiFi symbol

    content = Image.new("1", device.size, "black")
    draw = ImageDraw.Draw(content)

    # draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((39,1), str(fuel_level)+"%", font=font_bold, fill="white")
    # Add text and lines to the canvas
    draw.text((38, 30), "FUEL REMAINING", font=font_subtext, fill="white")
    status_line_x = 0
    status_line_y = 45
    status_line_length = 128
    draw.line([(status_line_x, status_line_y), (status_line_x + status_line_length, status_line_y)], fill="white", width=2)

    ## Drawing Wifi ##            
    # Draw WiFi symbol
    for i in range(num_arcs-1):
        # Calculate the position and size of each arc
        pos = [wifi_x - (i+1)*radius_increment, wifi_y - (i+1)*radius_increment,
            wifi_x + (i+1)*radius_increment, wifi_y + (i+1)*radius_increment]
        draw.arc(pos, start=225, end=315, fill="white", width=2)  # Adjust start and end angles to correct orientation
    
    
    wifi_y_pie = wifi_y + 2 

    pie_slice_radius =  3 
    pie_slice_pos = [
        wifi_x - pie_slice_radius, wifi_y_pie - pie_slice_radius,
        wifi_x + pie_slice_radius, wifi_y_pie + pie_slice_radius
    ]
    draw.pieslice(pie_slice_pos, start=225, end=315, fill="white")
    
    # Check internet connection status        
    line_base_x = 0
    line_base_y = 45
    line_length = 18

    if not internet_status:
        # If not connected, draw a line through the WiFi symbol, adjust coordinates to correct orientation
        draw.line([(line_base_x, line_base_y),
                (line_base_x + line_length-6, line_base_y + line_length)], fill="white", width=1)
        
    ## Module Status ##
    draw.text((20, 50), "STATUS: " + str(module_status), font=font_main_status, fill="white")

    ## Fuel Gauge ##
    # Define the position and radius for the gauge
    gauge_x = 20
    gauge_y = 20
    bg_rad = 18
    gauge_rad = 17

    # Calculate the position for the background arc and the gauge arc
    pos_bg = [gauge_x - bg_rad, gauge_y - bg_rad, gauge_x + bg_rad, gauge_y + bg_rad]
    pos_gauge = [gauge_x - gauge_rad, gauge_y - gauge_rad, gauge_x + gauge_rad, gauge_y + gauge_rad]

    # Define the fuel_remaining value (this should be updated dynamically in your actual code)
    fuel_remaining = abs(fuel_level - 100)  # for example, 50%

    # Calculate the start angle for the gauge arc based on the fuel_remaining value
    start_angle = (1 - fuel_remaining / 100) * 360 - 90

    # Draw the background arc
    draw.arc(pos_bg, start=0, end=360, fill="white", width=5)
    
    # # If this is called on start, play fuel gauge animation
    if boot_flag:
        # Gauge up
        for i in range (-90, 270, 5):
            # Draw the gauge arc
            draw.arc(pos_bg, start=0, end=360, fill="white", width=5)
            draw.arc(pos_gauge, start=i, end=270, fill="black", width=3)
            device.display(content)
            # Animation duration
            sleep(.008)

        # Gauge down to actual value
        for i in range (100, fuel_level, -1):
            draw.arc(pos_bg, start=0, end=360, fill="white", width=5)
            fuel_remaining_animation = abs(i - 100)
            start_angle_animation = (1 - fuel_remaining_animation / 100) * 360 - 90
            draw.arc(pos_gauge, start=start_angle_animation, end=270, fill="black", width=3)
            device.display(content)
            sleep(.025)

    else:
        draw.arc(pos_bg, start=0, end=360, fill="white", width=5)
        draw.arc(pos_gauge, start=start_angle, end=270, fill="black", width=3)

    device.display(content)
