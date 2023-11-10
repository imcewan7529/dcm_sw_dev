# screen_main.py

from PIL import Image
from PIL import ImageFont
from luma.core.render import canvas

def display(device):
    # ... your display logic and interactions for the main screen ...
    device.contrast(255) # Set contrast to max

    # Load the HNOI logo icon
    image_path = "hnoi_logo_icon.png"
    image = Image.open(image_path)

    # Load fonts
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=33)  # Adjust size as needed
    font_subtext = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=10)

    ## === IMAGE SCALING ===
    # Scale factor (for example, 0.8 for scaling down by 80%)
    scale_factor = 0.65

    # Resize the image
    resized_image = image.resize((int(image.width * scale_factor), int(image.height * scale_factor)))

    # Create a blank canvas of the OLED display size
    canvas_image = Image.new('1', (device.width, device.height))

    # Paste the smaller image onto the canvas
    canvas_image.paste(resized_image, (2, 10))

    ## === MAIN DRAWING ===

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")

        # Draw the canvas_image onto the canvas
        draw.bitmap((0, 0), canvas_image, fill="white")
        
        # Add text and lines to the canvas
        draw.text((42, 8), "HNO", font=font_bold, fill="white")
        draw.line([(44, 45), (125, 45)], fill="white", width=10)
        draw.text((44, 40), "INTERNATIONAL", font=font_subtext, fill="black")
